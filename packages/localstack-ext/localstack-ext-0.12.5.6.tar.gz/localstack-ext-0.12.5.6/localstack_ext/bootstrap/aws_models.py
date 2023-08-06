from localstack.utils.aws import aws_models
Czayt=super
CzayU=None
Czayj=id
class LambdaLayer(aws_models.LambdaFunction):
 def __init__(self,arn):
  Czayt(LambdaLayer,self).__init__(arn)
  self.cwd=CzayU
  self.runtime=''
  self.handler=''
  self.envvars={}
  self.versions={}
class BaseComponent(aws_models.Component):
 def name(self):
  return self.Czayj.split(':')[-1]
class RDSDatabase(BaseComponent):
 def __init__(self,Czayj,env=CzayU):
  Czayt(RDSDatabase,self).__init__(Czayj,env=env)
class RDSCluster(BaseComponent):
 def __init__(self,Czayj,env=CzayU):
  Czayt(RDSCluster,self).__init__(Czayj,env=env)
class AppSyncAPI(BaseComponent):
 def __init__(self,Czayj,env=CzayU):
  Czayt(AppSyncAPI,self).__init__(Czayj,env=env)
class AmplifyApp(BaseComponent):
 def __init__(self,Czayj,env=CzayU):
  Czayt(AmplifyApp,self).__init__(Czayj,env=env)
class ElastiCacheCluster(BaseComponent):
 def __init__(self,Czayj,env=CzayU):
  Czayt(ElastiCacheCluster,self).__init__(Czayj,env=env)
class TransferServer(BaseComponent):
 def __init__(self,Czayj,env=CzayU):
  Czayt(TransferServer,self).__init__(Czayj,env=env)
class CloudFrontDistribution(BaseComponent):
 def __init__(self,Czayj,env=CzayU):
  Czayt(CloudFrontDistribution,self).__init__(Czayj,env=env)
class CodeCommitRepository(BaseComponent):
 def __init__(self,Czayj,env=CzayU):
  Czayt(CodeCommitRepository,self).__init__(Czayj,env=env)
# Created by pyminifier (https://github.com/liftoff/pyminifier)
