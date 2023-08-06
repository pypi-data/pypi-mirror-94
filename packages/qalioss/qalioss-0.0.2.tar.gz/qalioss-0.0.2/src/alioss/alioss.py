# -*- coding: utf-8 -*-
import oss2
import os
from tqdm import tqdm
import time

class OSSession():
    def __init__(self,p1,p2,p3="tianchioss"):
        super().__init__()
        if p1 == "zwy" and p2 == "qwerty123":
            p1 = 'LTAI4GEJu3yAP3bFU2cYpp3G'
            p2 = 'etcbVtyzYB0pUAWErmh1WAD9YrABEx'
        self.auth = oss2.Auth(p1,p2)
        self.setBucket(p3)

    def setBucket(self,bucketName):
        self.bucket = oss2.Bucket(self.auth,endpoint="http://oss-cn-beijing.aliyuncs.com",bucket_name=bucketName)
        return self

    def download_obs_files(self,obs,local):
        """
        只要是文件夹都要使用"/"作为结束
        """
        if obs[-1] == "/":
            fileLists = self.get_allfiles_from_obs(obs)
            for i in tqdm(fileLists):
                self.download_single_obs_files(i,local,folder="/".join(i[len(obs):].split("/")[:-1]))
        else:
            self.download_single_obs_files(obs,local)

    def download_single_obs_files(self,obs,local,folder=""):
        """
        local should end with "/"
        """
        if folder:
            if not os.path.isdir(local+folder):
                os.mkdir(local+folder)
            self.bucket.get_object_to_file(obs, local+folder+"/"+obs.split("/")[-1])
        else:
            self.bucket.get_object_to_file(obs, local+obs.split("/")[-1])

    def get_allfiles_from_obs(self,obs):
        res = []
        for obj in oss2.ObjectIterator(self.bucket,prefix=obs):
            res.append(obj.key)
        return res

    def __download_single_obs_files(self,obs,local):
        self.bucket.get_object_to_file(obs,local)
        print("[INFO]",time.ctime(),"\t",obs,"\t has downloaded successfully")

    def upload_local_files(self,local,obs):
        if local[-1] == "/":
            self.upload_local_folder(local,obs)
        else:
            self.upload_local_single_files(local,obs)

    def upload_local_folder(self,local,obs):
        validPairs = self.makeValidPairs(local,obs)
        local = os.path.abspath(local)
        validPairsBar = tqdm(validPairs)
        for pairs in validPairsBar:
            self.upload_local_single_files(local+"/"+pairs[0],pairs[1])
            
    def upload_local_single_files(self,local,obs):
        self.bucket.put_object_from_file(obs,local)
        print(time.ctime(),"\t",local,"\t has uploaded success!!!")

    def makeValidPairs(self,local,obs):
        prefex = ""
        stack = []
        local = os.path.abspath(local)
        stack.append(local)
        res = []
        while stack:
            for i in range(len(stack)):
                now = stack.pop(0)
                if now == local:
                    prefex = ""
                else:
                    prefex = now[len(local)+1:].replace("\\",'/') + "/"
                files = os.listdir(now)
                for _file in files:
                    if os.path.isdir(os.path.join(now,_file)):
                        stack.append(os.path.join(now,_file))
                    else:
                        res.append((prefex+_file,obs+prefex+_file))    
        return res

if __name__ == "__main__":
    # print(makeValidPairs("./WangyangZuo/others/","model/"))
    # upload_local_files("./WangyangZuo/others/","model/")
    # get_allfiles_from_obs("model")
    session = OSSession("zwy","qwerty123")
    session.download_obs_files("model/","../../")