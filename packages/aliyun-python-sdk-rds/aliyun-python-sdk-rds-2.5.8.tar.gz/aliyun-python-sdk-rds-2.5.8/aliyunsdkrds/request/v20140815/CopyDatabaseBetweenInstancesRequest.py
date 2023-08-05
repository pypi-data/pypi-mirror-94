# Licensed to the Apache Software Foundation (ASF) under one
# or more contributor license agreements.  See the NOTICE file
# distributed with this work for additional information
# regarding copyright ownership.  The ASF licenses this file
# to you under the Apache License, Version 2.0 (the
# "License"); you may not use this file except in compliance
# with the License.  You may obtain a copy of the License at
#
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied.  See the License for the
# specific language governing permissions and limitations
# under the License.

from aliyunsdkcore.request import RpcRequest
from aliyunsdkrds.endpoint import endpoint_data

class CopyDatabaseBetweenInstancesRequest(RpcRequest):

	def __init__(self):
		RpcRequest.__init__(self, 'Rds', '2014-08-15', 'CopyDatabaseBetweenInstances','rds')
		self.set_method('POST')
		if hasattr(self, "endpoint_map"):
			setattr(self, "endpoint_map", endpoint_data.getEndpointMap())
		if hasattr(self, "endpoint_regional"):
			setattr(self, "endpoint_regional", endpoint_data.getEndpointRegional())


	def get_ResourceOwnerId(self):
		return self.get_query_params().get('ResourceOwnerId')

	def set_ResourceOwnerId(self,ResourceOwnerId):
		self.add_query_param('ResourceOwnerId',ResourceOwnerId)

	def get_DBInstanceId(self):
		return self.get_query_params().get('DBInstanceId')

	def set_DBInstanceId(self,DBInstanceId):
		self.add_query_param('DBInstanceId',DBInstanceId)

	def get_RestoreTime(self):
		return self.get_query_params().get('RestoreTime')

	def set_RestoreTime(self,RestoreTime):
		self.add_query_param('RestoreTime',RestoreTime)

	def get_BackupId(self):
		return self.get_query_params().get('BackupId')

	def set_BackupId(self,BackupId):
		self.add_query_param('BackupId',BackupId)

	def get_SyncUserPrivilege(self):
		return self.get_query_params().get('SyncUserPrivilege')

	def set_SyncUserPrivilege(self,SyncUserPrivilege):
		self.add_query_param('SyncUserPrivilege',SyncUserPrivilege)

	def get_DbNames(self):
		return self.get_query_params().get('DbNames')

	def set_DbNames(self,DbNames):
		self.add_query_param('DbNames',DbNames)

	def get_TargetDBInstanceId(self):
		return self.get_query_params().get('TargetDBInstanceId')

	def set_TargetDBInstanceId(self,TargetDBInstanceId):
		self.add_query_param('TargetDBInstanceId',TargetDBInstanceId)