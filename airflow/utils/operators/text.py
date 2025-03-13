import sys
sys.path.append('./airflow')
import polars as pl
import requests
import time
from PIL import Image
from io import BytesIO
from datetime import datetime
from pyvi import ViTokenizer
from transformers import AutoTokenizer


class TextOperator():
    @staticmethod
    def tokenize_vietnamese(text: str):
        tokens = ViTokenizer.tokenize(text).split(" ")
        return tokens

    @staticmethod
    def scaling_data(df:pl.DataFrame, selected_columns:list=None):
        if selected_columns != None:
            temp_df = df.select(selected_columns)
        else:
            temp_df = df.select('*')
        return temp_df

    @staticmethod
    def clean_caption(df:pl.DataFrame):
        regex_pattern = r'[!“"”#$%&()*+,./:;<=>?@\[\\\]\^{|}~-]'
        cleaned_df = df.with_columns(
            pl.lit(datetime.now()).alias("created_time"),
            pl.col("short_caption").str.to_lowercase().alias("short_caption"),
        ).with_columns(
            pl.col("short_caption").str.replace_all(regex_pattern, "").alias("short_caption")
        )
        cleaned_df = cleaned_df.with_columns(
            tokenized_caption=pl.col("short_caption")
                                .map_elements(lambda x: TextOperator.tokenize_vietnamese(x), return_dtype=pl.List(pl.String()))
                                .list.join(" ")
        )
        return cleaned_df

    @staticmethod
    def perform_imc(image_path, url):
        response = requests.post(url=url, json={"image_url": image_path,})
        print("Response in = ", response.elapsed.total_seconds())
        if response.status_code == 200:
            return response.json().get("response_message")
        else:
            print("Error:", response.status_code, response.text)
            return None
        
    @staticmethod
    def encode_caption(caption:str):
        # Load tokenizer của BartPho
        tokenizer = AutoTokenizer.from_pretrained("vinai/bartpho-word")
        # encode caption
        tokenized = tokenizer.encode_plus(caption, return_tensors="pt", padding="max_length", truncation=True)
        tokenized_dict = dict(tokenized)
        return tokenized_dict

    @staticmethod
    def load_image_from_url(url):
        """Load image from URL with resize"""
        try:
            response = requests.get(url, timeout=10, verify=False)  # Bỏ qua SSL verify
            response.raise_for_status()
            image = Image.open(BytesIO(response.content))
            
            # Resize image if too large
            max_size = (800, 800)  # Giới hạn kích thước tối đa
            if image.size[0] > max_size[0] or image.size[1] > max_size[1]:
                image.thumbnail(max_size, Image.Resampling.LANCZOS)
                
            return image
        except Exception as e:
            print(f"Error loading image from URL: {e}")
            return None

    @staticmethod
    def caption_generator(genai, image_url, prompt, max_retries=3):
        """Get prediction with retries"""
        for attempt in range(max_retries):
            try:
                model = genai.GenerativeModel('gemini-1.5-flash')
                image = TextOperator.load_image_from_url(image_url)
                if image is None:
                    return None

                response = model.generate_content([prompt, image])
                return response.text
                
            except Exception as e:
                if attempt == max_retries - 1:  # Last attempt
                    return None
                time.sleep(2 * (attempt + 1))  # Exponential backoff