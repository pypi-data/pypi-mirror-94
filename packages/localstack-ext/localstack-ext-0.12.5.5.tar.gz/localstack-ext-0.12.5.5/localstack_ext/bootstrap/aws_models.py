from localstack.utils.aws import aws_models
Kguih=super
Kguit=None
Kguiz=id
class LambdaLayer(aws_models.LambdaFunction):
 def __init__(self,arn):
  Kguih(LambdaLayer,self).__init__(arn)
  self.cwd=Kguit
  self.runtime=''
  self.handler=''
  self.envvars={}
  self.versions={}
class BaseComponent(aws_models.Component):
 def name(self):
  return self.Kguiz.split(':')[-1]
class RDSDatabase(BaseComponent):
 def __init__(self,Kguiz,env=Kguit):
  Kguih(RDSDatabase,self).__init__(Kguiz,env=env)
class RDSCluster(BaseComponent):
 def __init__(self,Kguiz,env=Kguit):
  Kguih(RDSCluster,self).__init__(Kguiz,env=env)
class AppSyncAPI(BaseComponent):
 def __init__(self,Kguiz,env=Kguit):
  Kguih(AppSyncAPI,self).__init__(Kguiz,env=env)
class AmplifyApp(BaseComponent):
 def __init__(self,Kguiz,env=Kguit):
  Kguih(AmplifyApp,self).__init__(Kguiz,env=env)
class ElastiCacheCluster(BaseComponent):
 def __init__(self,Kguiz,env=Kguit):
  Kguih(ElastiCacheCluster,self).__init__(Kguiz,env=env)
class TransferServer(BaseComponent):
 def __init__(self,Kguiz,env=Kguit):
  Kguih(TransferServer,self).__init__(Kguiz,env=env)
class CloudFrontDistribution(BaseComponent):
 def __init__(self,Kguiz,env=Kguit):
  Kguih(CloudFrontDistribution,self).__init__(Kguiz,env=env)
class CodeCommitRepository(BaseComponent):
 def __init__(self,Kguiz,env=Kguit):
  Kguih(CodeCommitRepository,self).__init__(Kguiz,env=env)
# Created by pyminifier (https://github.com/liftoff/pyminifier)
