from localstack.utils.aws import aws_models
OEYwB=super
OEYwz=None
OEYwM=id
class LambdaLayer(aws_models.LambdaFunction):
 def __init__(self,arn):
  OEYwB(LambdaLayer,self).__init__(arn)
  self.cwd=OEYwz
  self.runtime=''
  self.handler=''
  self.envvars={}
  self.versions={}
class BaseComponent(aws_models.Component):
 def name(self):
  return self.OEYwM.split(':')[-1]
class RDSDatabase(BaseComponent):
 def __init__(self,OEYwM,env=OEYwz):
  OEYwB(RDSDatabase,self).__init__(OEYwM,env=env)
class RDSCluster(BaseComponent):
 def __init__(self,OEYwM,env=OEYwz):
  OEYwB(RDSCluster,self).__init__(OEYwM,env=env)
class AppSyncAPI(BaseComponent):
 def __init__(self,OEYwM,env=OEYwz):
  OEYwB(AppSyncAPI,self).__init__(OEYwM,env=env)
class AmplifyApp(BaseComponent):
 def __init__(self,OEYwM,env=OEYwz):
  OEYwB(AmplifyApp,self).__init__(OEYwM,env=env)
class ElastiCacheCluster(BaseComponent):
 def __init__(self,OEYwM,env=OEYwz):
  OEYwB(ElastiCacheCluster,self).__init__(OEYwM,env=env)
class TransferServer(BaseComponent):
 def __init__(self,OEYwM,env=OEYwz):
  OEYwB(TransferServer,self).__init__(OEYwM,env=env)
class CloudFrontDistribution(BaseComponent):
 def __init__(self,OEYwM,env=OEYwz):
  OEYwB(CloudFrontDistribution,self).__init__(OEYwM,env=env)
class CodeCommitRepository(BaseComponent):
 def __init__(self,OEYwM,env=OEYwz):
  OEYwB(CodeCommitRepository,self).__init__(OEYwM,env=env)
# Created by pyminifier (https://github.com/liftoff/pyminifier)
