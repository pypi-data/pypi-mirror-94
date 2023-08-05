import os
import boto3
import typeguard
from botocore.exceptions import ClientError
from os import listdir
from os.path import isfile, join

from cloud_governance.common.logger.logger_time_stamp import logger_time_stamp


class S3Operations:
    """ This class is responsible for S3 operations """

    def __init__(self, region_name):
        self.__s3_client = boto3.client('s3', region_name=region_name)

    @logger_time_stamp
    @typeguard.typechecked
    def upload_file(self, file_name_path: str, bucket: str, key: str, upload_file: str):
        """
        This method upload file to s3
        STANDARD_IA , ONEZONE_IA , INTELLIGENT_TIERING , GLACIER , or DEEP_ARCHIVE
        :param file_name_path:'D:\\Performance\\Projects\\py-image-service\\data\\data\\DJI_0100.jpg'
        :param bucket:'devops-ais'
        :param key:'test-data'
        :param upload_file:'DJI_0100.jpg'
        :return:
        """

        try:
            self.__s3_client.upload_file(Filename=file_name_path,
                                         Bucket=bucket,
                                         Key=f'{key}/{upload_file}',
                                         ExtraArgs={'ServerSideEncryption': 'AES256',
                                                    'StorageClass': 'ONEZONE_IA'})
        # Todo add custom error
        except ClientError:
            raise
        except Exception:
            raise

    @logger_time_stamp
    @typeguard.typechecked
    def download_file(self, bucket: str, key: str, download_file: str, file_name_path: str):
        """
        This method download file from s3
        :param bucket:'devops-ais'
        :param key:'logs/ec2-idle/2021/01/19/18'
        :param download_file: 'DJI_0100.jpg'
        :param file_name_path:'D:\\Performance\\Projects\\py-image-service\\data\\rt_results\\DJI_0100.jpg'
        :return:
        """
        try:
            if download_file:
                self.__s3_client.download_file(Bucket=bucket, Key=f'{key}/{download_file}', Filename=file_name_path)
            else:
                self.__s3_client.download_file(Bucket=bucket, Key=key, Filename=file_name_path)
        # Todo add custom error
        except ClientError:
            raise
        except Exception:
            raise

    @logger_time_stamp
    @typeguard.typechecked
    def delete_file(self, bucket: str, key: str, file_name: str):
        """
        This method download file from s3
        :param bucket:'devops-ais'
        :param key:'test-data'
        :param delete_file: 'DJI_0100.jpg'
        :param file_name_path:'D:\\Performance\\Projects\\py-image-service\\data\\rt_results\\DJI_0100.jpg'
        :return:
        """
        try:
            self.__s3_client.delete_object(Bucket=bucket, Key=f'{key}/{file_name}')
        # Todo add custom error
        except ClientError:
            raise
        except Exception:
            raise

    @logger_time_stamp
    @typeguard.typechecked
    def delete_folder(self, bucket: str, key: str):
        """
        This method download file from s3
        :param bucket:'devops-ais'
        :param key:'framework/test'
        :return:
        """
        try:
            objects_to_delete = self.__s3_client.list_objects(Bucket=bucket, Prefix=key)
            delete_keys = {
                'Objects': [{'Key': k} for k in [obj['Key'] for obj in objects_to_delete.get('Contents', [])]]}
            if delete_keys['Objects']:
                self.__s3_client.delete_objects(Bucket=bucket, Delete=delete_keys)
        # Todo add custom error
        except ClientError:
            raise
        except Exception:
            raise

    @logger_time_stamp
    @typeguard.typechecked
    def create_folder(self, bucket: str, key: str):
        """
        This method download file from s3
        :param bucket:'devops-ais'
        :param key:'framework/test'
        :return:
        """
        try:
            self.__s3_client.put_object(Bucket=bucket, Key=key)
        # Todo add custom error
        except ClientError:
            raise
        except Exception:
            raise

    @logger_time_stamp
    @typeguard.typechecked
    def file_exist(self, bucket: str, key: str, file_name: str):
        """
        This method check if file exist
        :param bucket:'devops-ais'
        :param key:'framework/test'
        :param file_name:'file.txt'
        :return:
        """
        try:
            response = self.__s3_client.list_objects_v2(Bucket=bucket, Prefix=key)
            if response.get('Contents'):
                for item in response['Contents']:
                    if file_name in item['Key']:
                        return True
            return False

        # Todo add custom error
        except ClientError:
            raise
        except Exception:
            raise

    @logger_time_stamp
    @typeguard.typechecked
    def upload_objects(self, local_source: str, s3_target: str):
        """
        This method upload local data folder to s3 target path
        :param local_source: local data folder i.e. 'D:/Temp/'
        :param s3_target: target s3 path i.e. 'data_store/calc_image_data/'
        :return:
        """
        try:
            if '/' in s3_target:
                targets = s3_target.split('/')
                bucket = targets[0]
                key = '/'.join(targets[1:])
            else:
                bucket = s3_target
                key = ''

            files = [f for f in listdir(local_source) if isfile(join(local_source, f))]
            for file in files:
                filename = os.path.join(local_source, file)
                self.upload_file(file_name_path=filename, bucket=bucket, key=key, upload_file=file)

        # Todo add custom error
        except ClientError as err:
            raise
        except Exception:
            raise

    @logger_time_stamp
    @typeguard.typechecked
    def download_objects(self, s3_target: str, local_source: str):
        """
        This method download from s3 target to local data folder
        :param local_source: local data folder i.e. 'D:/Temp/'
        :param s3_target: target s3 path i.e. 'data_store/calc_image_data/'
        :return:
        """
        files = []

        try:
            if '/' in s3_target:
                targets = s3_target.split('/')
                bucket = targets[0]
                key = '/'.join(targets[1:])
            else:
                bucket = s3_target
                key = ''

            response = self.__s3_client.list_objects_v2(Bucket=bucket, Prefix=key)
            if response.get('Contents'):
                for item in response['Contents']:
                    if item['Key'].split('/')[-1]:
                        files.append(item['Key'].split('/')[-1])
                    else:
                        files.append(item['Key'])

            for file in files:
                file_name = os.path.join(local_source, file)
                self.download_file(bucket=bucket, key=key, download_file=file, file_name_path=file_name)

        # Todo add custom error
        except ClientError as err:
            raise
        except Exception:
            raise

    @logger_time_stamp
    @typeguard.typechecked
    def get_last_objects(self, bucket: str, logs_dir: str, policy: str):
        """
        This method return last object per policy, only path without file name
        @param bucket:
        @param dir:
        @param policy:
        @return:
        """
        try:
            if '_' in policy:
                policy = policy.replace('_', '-')
            objs = self.__s3_client.list_objects_v2(Bucket=bucket,
                                                    Prefix=f'{logs_dir}/{policy}',
                                                    MaxKeys=100)['Contents']
        except:
            return None
        get_last_modified = lambda obj: int(obj['LastModified'].strftime('%s'))
        full_path = [obj['Key'] for obj in sorted(objs, key=get_last_modified)][-1]
        return os.path.dirname(full_path)
