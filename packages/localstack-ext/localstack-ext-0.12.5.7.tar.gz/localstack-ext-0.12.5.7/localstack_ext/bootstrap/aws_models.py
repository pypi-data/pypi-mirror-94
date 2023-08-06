from localstack.utils.aws import aws_models
msnLX=super
msnLj=None
msnLB=id
class LambdaLayer(aws_models.LambdaFunction):
 def __init__(self,arn):
  msnLX(LambdaLayer,self).__init__(arn)
  self.cwd=msnLj
  self.runtime=''
  self.handler=''
  self.envvars={}
  self.versions={}
class BaseComponent(aws_models.Component):
 def name(self):
  return self.msnLB.split(':')[-1]
class RDSDatabase(BaseComponent):
 def __init__(self,msnLB,env=msnLj):
  msnLX(RDSDatabase,self).__init__(msnLB,env=env)
class RDSCluster(BaseComponent):
 def __init__(self,msnLB,env=msnLj):
  msnLX(RDSCluster,self).__init__(msnLB,env=env)
class AppSyncAPI(BaseComponent):
 def __init__(self,msnLB,env=msnLj):
  msnLX(AppSyncAPI,self).__init__(msnLB,env=env)
class AmplifyApp(BaseComponent):
 def __init__(self,msnLB,env=msnLj):
  msnLX(AmplifyApp,self).__init__(msnLB,env=env)
class ElastiCacheCluster(BaseComponent):
 def __init__(self,msnLB,env=msnLj):
  msnLX(ElastiCacheCluster,self).__init__(msnLB,env=env)
class TransferServer(BaseComponent):
 def __init__(self,msnLB,env=msnLj):
  msnLX(TransferServer,self).__init__(msnLB,env=env)
class CloudFrontDistribution(BaseComponent):
 def __init__(self,msnLB,env=msnLj):
  msnLX(CloudFrontDistribution,self).__init__(msnLB,env=env)
class CodeCommitRepository(BaseComponent):
 def __init__(self,msnLB,env=msnLj):
  msnLX(CodeCommitRepository,self).__init__(msnLB,env=env)
# Created by pyminifier (https://github.com/liftoff/pyminifier)
