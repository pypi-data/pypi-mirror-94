class kitinv1:
	"""docstring for ClassName"""
	def gip():
		import math
		a = float(input('Введите сторону а: '))
		b = float(input('Введите сторону b: '))
		c = (a*a)* (b*b)
		print(math.sqrt(c))

	def so():
		import math
		a = float(input('Введите радиус окружности: '))
		b = 2* a * 3.14
		c = 3.14*a*a
		
		print("Длинна окружности равна "+str(b))
		print("S окружности равна "+str(c))


	def h():
		
		a = float(input('Первое число: '))
		b = float(input('Второе число: '))
		c = float(input('Третье число: '))

		d = (a+b+c)/3
		
		
		print("Среднее арифметическое число = "+str(d))


	def s():
		
		a = float(input('Расстояние составляет: '))
		b = float(input('Средняя скорость движения: '))
		c = (a / b) * 60

		
		
		
		print("Время до школы = "+str(c)+' мин')


	def sh():
		
		a = float(input('Расстояние составляет: '))
		b = float(input('Средняя скорость движения: '))
		c = (a / b) 

		
		
		
		print("Время до школы = "+str(c)+' ч')


	def ch():
		v = input("Введите 2-х значное число")

		ff = int(v[0])

		s = int(v[1])

		print("сумма: "+str(ff + s)+"")

		print("произведение: "+str(ff * s)+"")

		print("перестановка: "+str(s)+""+str(ff)+"")
			

