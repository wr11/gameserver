# -*- coding: utf-8 -*-

import pymysql
import pymysql.cursors
import msgpack
import pubdefines

MYSQL_SELECT = 1
MYSQL_INSERT = 2
MYSQL_UPDATE = 3
MYSQL_MANUAL = 4
MYSQL_HANDLE_TYPE = [MYSQL_SELECT, MYSQL_INSERT, MYSQL_UPDATE, MYSQL_MANUAL]

class CMysqlBase:

	"""
	m_ColName 必有data列
	"""

	m_Type = ""		#子类需对该属性重新赋值
	m_TblName = ""
	m_ColName = ["data"]

	def __init__(self, sCursorType=pubdefines.MYSQL_DICTCURSOR, sColNmae = ""):
		self.m_Config = {
			"host":'localhost',
			"user":'root',
			"password":'mytool2021',
			"db":'mytool_db',
			"charset":'utf8',
			"cursorclass":eval("pymysql.cursors.%s" % sCursorType),
		}
		self.m_State = 1		#数据库查询状态 1-无查询，可以操作 0-正在查询，不可操作  todo目前不是异步，不用判断此状态
		self.m_Data = {}
		self.m_Conn = self.MakeConnection()
		self.m_CursorType = sCursorType
		if sColNmae:
			self.m_ColName.append(sColNmae)

	def __repr__(self):
		cls = self.__class__
		return "<%s %s(%d) at %s>" % (cls.__module__, cls.__name__, self.m_Type, self.m_State)

	def __del__(self):
		self.m_Conn.close()

	def MakeConnection(self):
		return pymysql.connect(**self.m_Config)

	def CheckConfig(self):
		assert self.m_Type and self.m_TblName, "mysqlbase config wrong"

	def GenerateSqlStatement(self, iType, **kwargs):
		"""
		kwargs param:
		Filter: col_name >/</=/!= value 条件
		SetValue： col_name1 = value1, col_name2 = value2 设值
		"""
		if iType == MYSQL_SELECT:			#查询语句
			sFilter = kwargs.get("Filter")
			assert sFilter
			return "SELECT * FROM %s WHERE %s;" % (self. m_TblName, sFilter)
		elif iType == MYSQL_INSERT:		#插入语句
			sSetValue = kwargs.get("SetValue")
			assert sSetValue
			return "INSERT INTO %s SET %s;" % (self. m_TblName, sSetValue)
		elif iType == MYSQL_UPDATE:		#更新语句
			sFilter = kwargs.get("Filter")
			sSetValue = kwargs.get("SetValue")
			assert sFilter and sSetValue
			return "UPDATE %s SET %s WHERE %s;" % (self. m_TblName, sSetValue, sFilter)

	def Handler(self, iType, **kwargs):
		"""
		kwargs param:
		Statement: 自定义语句
		"""
		self.CheckConfig()
		if iType not in MYSQL_HANDLE_TYPE:
			print("数据库操作类型错误")
			return
		with self.m_Conn.cursor() as oCursor:
			if iType == MYSQL_MANUAL:
				sSqlState = kwargs.get("Statement")
			else:
				sSqlState = self.GenerateSqlStatement(iType, **kwargs)
			oCursor.execute(sSqlState)
			result = oCursor.fetchall()
		self.m_Conn.commit()

		self.ResultInterrupt(result)
		return result

	#todo 需要支持其他游标类型的解析
	def ResultInterrupt(self, result):
		if self.m_CursorType == pubdefines.MYSQL_DICTCURSOR:
			pass
		elif self.m_CursorType == pubdefines.MYSQL_CURSOR:
			pass
		else:
			pass


	def LoadAll(self):
		self.CheckConfig()

	def SaveAll(self):
		self.CheckConfig()

	def Save(self):
		pass


#test
class CTestSql(CMysqlBase):

	m_Type = "test"
	m_TblName = "test"


def main():
	oTestMysql = CTestSql(pubdefines.MYSQL_DICTCURSOR, "test")
	oTestMysql.Handler(MYSQL_INSERT, SetValue = "id=15332342922,test=123")
	oTestMysql.Handler(MYSQL_SELECT, Filter = "test=123")
	oTestMysql.Handler(MYSQL_UPDATE, SetValue = "test=124", Filter = "test=123")
	result = oTestMysql.Handler(MYSQL_SELECT, Filter = "test=124")
	result=oTestMysql.Handler(MYSQL_MANUAL, Statement = "select id from %s"%oTestMysql.m_TblName)

	print(result)