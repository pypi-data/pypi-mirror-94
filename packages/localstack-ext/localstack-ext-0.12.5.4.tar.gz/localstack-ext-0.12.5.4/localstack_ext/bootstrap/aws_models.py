from localstack.utils.aws import aws_models
JGuty=super
JGuta=None
JGutW=id
class LambdaLayer(aws_models.LambdaFunction):
 def __init__(self,arn):
  JGuty(LambdaLayer,self).__init__(arn)
  self.cwd=JGuta
  self.runtime=''
  self.handler=''
  self.envvars={}
  self.versions={}
class BaseComponent(aws_models.Component):
 def name(self):
  return self.JGutW.split(':')[-1]
class RDSDatabase(BaseComponent):
 def __init__(self,JGutW,env=JGuta):
  JGuty(RDSDatabase,self).__init__(JGutW,env=env)
class RDSCluster(BaseComponent):
 def __init__(self,JGutW,env=JGuta):
  JGuty(RDSCluster,self).__init__(JGutW,env=env)
class AppSyncAPI(BaseComponent):
 def __init__(self,JGutW,env=JGuta):
  JGuty(AppSyncAPI,self).__init__(JGutW,env=env)
class AmplifyApp(BaseComponent):
 def __init__(self,JGutW,env=JGuta):
  JGuty(AmplifyApp,self).__init__(JGutW,env=env)
class ElastiCacheCluster(BaseComponent):
 def __init__(self,JGutW,env=JGuta):
  JGuty(ElastiCacheCluster,self).__init__(JGutW,env=env)
class TransferServer(BaseComponent):
 def __init__(self,JGutW,env=JGuta):
  JGuty(TransferServer,self).__init__(JGutW,env=env)
class CloudFrontDistribution(BaseComponent):
 def __init__(self,JGutW,env=JGuta):
  JGuty(CloudFrontDistribution,self).__init__(JGutW,env=env)
class CodeCommitRepository(BaseComponent):
 def __init__(self,JGutW,env=JGuta):
  JGuty(CodeCommitRepository,self).__init__(JGutW,env=env)
# Created by pyminifier (https://github.com/liftoff/pyminifier)
