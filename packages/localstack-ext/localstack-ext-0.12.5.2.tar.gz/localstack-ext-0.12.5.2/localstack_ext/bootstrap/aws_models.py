from localstack.utils.aws import aws_models
YDPvE=super
YDPvj=None
YDPvz=id
class LambdaLayer(aws_models.LambdaFunction):
 def __init__(self,arn):
  YDPvE(LambdaLayer,self).__init__(arn)
  self.cwd=YDPvj
  self.runtime=''
  self.handler=''
  self.envvars={}
  self.versions={}
class BaseComponent(aws_models.Component):
 def name(self):
  return self.YDPvz.split(':')[-1]
class RDSDatabase(BaseComponent):
 def __init__(self,YDPvz,env=YDPvj):
  YDPvE(RDSDatabase,self).__init__(YDPvz,env=env)
class RDSCluster(BaseComponent):
 def __init__(self,YDPvz,env=YDPvj):
  YDPvE(RDSCluster,self).__init__(YDPvz,env=env)
class AppSyncAPI(BaseComponent):
 def __init__(self,YDPvz,env=YDPvj):
  YDPvE(AppSyncAPI,self).__init__(YDPvz,env=env)
class AmplifyApp(BaseComponent):
 def __init__(self,YDPvz,env=YDPvj):
  YDPvE(AmplifyApp,self).__init__(YDPvz,env=env)
class ElastiCacheCluster(BaseComponent):
 def __init__(self,YDPvz,env=YDPvj):
  YDPvE(ElastiCacheCluster,self).__init__(YDPvz,env=env)
class TransferServer(BaseComponent):
 def __init__(self,YDPvz,env=YDPvj):
  YDPvE(TransferServer,self).__init__(YDPvz,env=env)
class CloudFrontDistribution(BaseComponent):
 def __init__(self,YDPvz,env=YDPvj):
  YDPvE(CloudFrontDistribution,self).__init__(YDPvz,env=env)
class CodeCommitRepository(BaseComponent):
 def __init__(self,YDPvz,env=YDPvj):
  YDPvE(CodeCommitRepository,self).__init__(YDPvz,env=env)
# Created by pyminifier (https://github.com/liftoff/pyminifier)
