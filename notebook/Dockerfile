FROM jupyter/all-spark-notebook:python-3.9.13

USER root 

RUN curl -O https://archive.apache.org/dist/spark/spark-3.3.2/spark-3.3.2-bin-hadoop3.tgz \
    && tar zxvf spark-3.3.2-bin-hadoop3.tgz \
    && rm -rf spark-3.3.2-bin-hadoop3.tgz \
    && mv spark-3.3.2-bin-hadoop3/ /usr/local/ \
    && rm -rf /usr/local/spark \
    && rm -rf /usr/local/spark-3.3.0-bin-hadoop3 \
    && ln -s /usr/local/spark-3.3.2-bin-hadoop3 /usr/local/spark

RUN curl -O https://repo1.maven.org/maven2/software/amazon/awssdk/s3/2.18.41/s3-2.18.41.jar \
    && curl -O https://repo1.maven.org/maven2/com/amazonaws/aws-java-sdk/1.12.367/aws-java-sdk-1.12.367.jar \
    && curl -O https://repo1.maven.org/maven2/com/amazonaws/aws-java-sdk-bundle/1.11.1026/aws-java-sdk-bundle-1.11.1026.jar \
    && curl -O https://repo1.maven.org/maven2/org/apache/hadoop/hadoop-aws/3.3.2/hadoop-aws-3.3.2.jar \
    && curl -O https://repo1.maven.org/maven2/org/apache/hadoop/hadoop-common/3.3.2/hadoop-common-3.3.2.jar\
    && curl -O https://repo1.maven.org/maven2/io/delta/delta-core_2.12/2.3.0/delta-core_2.12-2.3.0.jar \
    && curl -O https://repo1.maven.org/maven2/io/delta/delta-storage/2.3.0/delta-storage-2.3.0.jar \
    # && curl -O https://repo1.maven.org/maven2/org/apache/spark/spark-sql-kafka-0-10_2.12/3.2.0/spark-sql-kafka-0-10_2.12-3.2.0.jar \
    # && curl -O https://repo1.maven.org/maven2/org/apache/spark/spark-token-provider-kafka-0-10_2.12/3.2.0/spark-token-provider-kafka-0-10_2.12-3.2.0.jar \
    # && curl -O https://repo1.maven.org/maven2/org/apache/kafka/kafka-clients/2.8.0/kafka-clients-2.8.0.jar \
    && curl -O https://repo1.maven.org/maven2/org/mongodb/spark/mongo-spark-connector/10.0.2/mongo-spark-connector-10.0.2.jar \
    && curl -O https://repo1.maven.org/maven2/org/mongodb/mongodb-driver-core/4.5.1/mongodb-driver-core-4.5.1.jar \
    && curl -O https://repo1.maven.org/maven2/org/mongodb/mongodb-driver-sync/4.5.1/mongodb-driver-sync-4.5.1.jar \
    && curl -O https://repo1.maven.org/maven2/org/mongodb/bson/4.5.1/bson-4.5.1.jar \
    && mv s3-2.18.41.jar /usr/local/spark/jars \
    && mv aws-java-sdk-1.12.367.jar /usr/local/spark/jars \
    && mv aws-java-sdk-bundle-1.11.1026.jar /usr/local/spark/jars \
    && mv hadoop-aws-3.3.2.jar /usr/local/spark/jars \
    && mv hadoop-common-3.3.2.jar /usr/local/spark/jars \
    && mv delta-core_2.12-2.3.0.jar /usr/local/spark/jars \
    && mv delta-storage-2.3.0.jar /usr/local/spark/jars \
    # && mv spark-sql-kafka-0-10_2.12-3.2.0.jar /opt/bitnami/spark/jars \
    # && mv spark-token-provider-kafka-0-10_2.12-3.2.0.jar /opt/bitnami/spark/jars \
    # && mv kafka-clients-2.8.0.jar /opt/bitnami/spark/jars \
    && mv mongo-spark-connector-10.0.2.jar /usr/local/spark/jars \
    && mv mongodb-driver-core-4.5.1.jar /usr/local/spark/jars \
    && mv mongodb-driver-sync-4.5.1.jar /usr/local/spark/jars \
    && mv bson-4.5.1.jar /usr/local/spark/jars

    
COPY ./requirements.txt .
RUN pip install -r requirements.txt
