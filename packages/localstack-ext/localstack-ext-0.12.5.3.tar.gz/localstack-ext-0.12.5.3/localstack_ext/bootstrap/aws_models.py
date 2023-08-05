from localstack.utils.aws import aws_models
pxSye=super
pxSyn=None
pxSyk=id
class LambdaLayer(aws_models.LambdaFunction):
 def __init__(self,arn):
  pxSye(LambdaLayer,self).__init__(arn)
  self.cwd=pxSyn
  self.runtime=''
  self.handler=''
  self.envvars={}
  self.versions={}
class BaseComponent(aws_models.Component):
 def name(self):
  return self.pxSyk.split(':')[-1]
class RDSDatabase(BaseComponent):
 def __init__(self,pxSyk,env=pxSyn):
  pxSye(RDSDatabase,self).__init__(pxSyk,env=env)
class RDSCluster(BaseComponent):
 def __init__(self,pxSyk,env=pxSyn):
  pxSye(RDSCluster,self).__init__(pxSyk,env=env)
class AppSyncAPI(BaseComponent):
 def __init__(self,pxSyk,env=pxSyn):
  pxSye(AppSyncAPI,self).__init__(pxSyk,env=env)
class AmplifyApp(BaseComponent):
 def __init__(self,pxSyk,env=pxSyn):
  pxSye(AmplifyApp,self).__init__(pxSyk,env=env)
class ElastiCacheCluster(BaseComponent):
 def __init__(self,pxSyk,env=pxSyn):
  pxSye(ElastiCacheCluster,self).__init__(pxSyk,env=env)
class TransferServer(BaseComponent):
 def __init__(self,pxSyk,env=pxSyn):
  pxSye(TransferServer,self).__init__(pxSyk,env=env)
class CloudFrontDistribution(BaseComponent):
 def __init__(self,pxSyk,env=pxSyn):
  pxSye(CloudFrontDistribution,self).__init__(pxSyk,env=env)
class CodeCommitRepository(BaseComponent):
 def __init__(self,pxSyk,env=pxSyn):
  pxSye(CodeCommitRepository,self).__init__(pxSyk,env=env)
# Created by pyminifier (https://github.com/liftoff/pyminifier)
