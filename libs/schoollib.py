from datetime import datetime
from DBcm import UseDatabase
import hashlib
import pytz

class SchoolData():
	def __init__(self, dbconfig):
		self.dbconfig = dbconfig

	def get_time(self):
		timezone = pytz.timezone('America/Sao_Paulo')
		self.agora = datetime.now(timezone)
		self.dia = self.agora.strftime('%A')
		self.hora = int(self.agora.strftime('%H'))
		self.data = self.agora.day
		self.minuto = int(self.agora.strftime('%M'))

	def horario(self):
		""" 11 = lanche manha
			12 = aumoço
			13 = lanche tarde """
		agora = '0'
		self.get_time()
		match self.hora:
			case 7:
				if 50 <= self.minuto < 59:
					agora = '2'
				elif 0 <= self.minuto < 49:
					agora = '1'

			case 8:
				if 0 <= self.minuto < 40:
					agora = '2'
				elif 39 <= self.minuto < 59:
					agora = '3'

			case 9:
				if 0 <= self.minuto < 29:
					agora = '3'
				elif 30 <= self.minuto < 49:
					agora = '11'
				elif 50 <= self.minuto < 59:
					agora = '4'

			case 10:
				if 0 <= self.minuto < 39:
					agora = '4'
				elif 40 <= self.minuto < 59:
					agora = '5'

			case 11:
				if 0 <= self.minuto < 29:
					agora = '5'
				elif 30 <= self.minuto < 59:
					agora = '12'

			case 12:
				if 0 <= self.minuto < 59:
					agora = '12'

			case 13:
				if 0 <= self.minuto < 49:
					agora = '6'
				elif 50 <= self.minuto < 59:
					agora = '7'

			case 14:
				if 0 <= self.minuto < 39:
					agora = '7'
				elif 40 <= self.minuto < 49:
					agora = '13'
				elif 50 <= self.minuto < 59:
					agora = '8'

			case 15:
				if 0 <= self.minuto < 39:
					agora = '8'
				elif 40 <= self.minuto < 59:
					agora = '9'

			case 16:
				if 0 <= self.minuto < 29:
					agora = '9'

			case _:
				agora = '0'
		return agora


	def aula(self, sala):
		""" aulas dict
			sala -> dia -> aula -> (matéria, professor) """
		self.get_time()
		horario = self.horario()
		if horario in ('11', '12', '13', '0'):
			return ('Nada','Nenhum')
		if self.dia in ('Saturday', 'Sunday'):
			return ('Nada', 'Nenhum')
		with UseDatabase(self.dbconfig) as cursor:
			sql = '''select materia, prof from aulas
			where dia = %s and sala = %s and horario = %s'''
			cursor.execute(sql, (self.dia, sala, horario))
			results = cursor.fetchone()
		return results

	def almoco(self, turma):
		self.get_time()
		new_turma = list(turma).pop(0)
		if self.data in list(range(1, 31, 3)):
			ordem = ('1', '2', '3')
		elif self.data in list(range(2, 31, 3)):
			ordem = ('3', '1', '2')
		elif self.data in list(range(3, 31, 3)):
			ordem = ('2', '3', '1')
		return {'ordem' : ordem, 'pos_sala' : (ordem.index(new_turma)+1)}
