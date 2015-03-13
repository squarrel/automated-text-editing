# -*- coding: utf-8 -*-
# .doc u text; cirilica u latinicu; popunjavanje html kartona
# .doc to text; cyrillic to latin; write to html file

import os
import sys

class Projekat():
	
	tekst = ''
	ime_fajla = ''
	studijski_program = ''
	naziv_predmeta = ''
	nastavnik = ''
	status_predmeta = ''
	espb = ''
	uslov = ''
	opis_predmeta = ''
	teorijska_nastava = ''
	prakticna_nastava = ''
	literatura = ''
	
	def doc_txt_catdoc(self, filename):
		(fi, fo, fe) = os.popen3('catdoc -w "%s"' % filename)
    
		fi.close()
		retval = fo.read()
		erroroutput = fe.read()
		fo.close()
		fe.close()

		self.tekst = retval
		#print self.tekst
	
		if not erroroutput:
			return retval
		else:
			raise OSError("Executing the command caused an error: %s" % erroroutput)

	def cir_u_lat(self):
		symbols = (u"абвгдђежзијклмнопрстћуфхцчшАБВГДЂЕЖЗИЈКЛМНОПРСТЋУФХЦЧШ",
					u"abvgdđežzijklmnoprstćufhcčšABVGDĐEŽZIJKLMNOPRSTĆUFHCČŠ")

		tr = {ord(a):ord(b) for a, b in zip(*symbols)}

		sequence = {
			u'љ':u'lj',
			u'њ':u'nj',
			u'џ':u'dž',
			u'Љ':u'Lj',
			u'Њ':u'Nj',
			u'Џ':u'Dž'
		}

		#text = u'абвгдђежзијклљмнњопрстћуфхцчџшАБВГДЂЕЖЗИЈКЛЉМНЊОПРСТЋУФХЦЧЏШ'
		text = self.tekst.decode('UTF-8')
	
		for char in sequence.keys():
			text = text.replace(char, sequence[char])
		self.tekst = text.translate(tr)
		#print self.tekst

	def izdvoj(self):
		f = open('test2', 'w')
		text = self.tekst.encode('UTF-8')
		f.write(text)
		f = open('test2', 'r')
		
		for line in f:
			if 'Vrsta i nivo studija' in line:
				self.studijski_program = line[22:]
				self.studijski_program = self.studijski_program.strip('\n')
				print '-'+self.studijski_program+'-'
			if 'Naziv predmeta' in line:
				#print line[16:]
				self.naziv_predmeta = line[16:]
				self.naziv_predmeta =  self.naziv_predmeta.strip('\n')
				print '-'+self.naziv_predmeta+'-'
				
				self.ime_fajla = line[-6:]
				self.ime_fajla = self.ime_fajla.strip('\n') + '.html'
				print '-'+self.ime_fajla+'-'
			if 'Nastavnik' in line:
				#print line
				self.nastavnik = line[11:]
				self.nastavnik = self.nastavnik.strip('\n')
				print '-'+self.nastavnik+'-'
			if 'Status predmeta' in line:
				#print line
				self.status_predmeta = line[17:]
				self.status_predmeta = self.status_predmeta.strip('\n')
				print '-'+self.status_predmeta+'-'
			if 'Broj ESPB' in line:
				#print line
				self.espb = line[11:]
				self.espb = self.espb.strip('\n')
				print '-'+self.espb+'-'
			if 'Uslov' in line:
				#print line
				self.uslov = line[7:]
				self.uslov = self.uslov.strip('\n')
				print '-'+self.uslov+'-'
			if 'Cilj predmeta' in line:
				a = f.next()
				self.opis_predmeta += a.strip('\n') + ' '
				#self.opis_predmeta = line[15:]
				#print self.opis_predmeta
			if 'Ishod predmeta' in line:
				b = f.next()
				self.opis_predmeta += b
				#self.opis_predmeta += line[16:]
				print 'Opis predmeta: '+'-'+self.opis_predmeta+'-'
			if 'Teorijska nastava' in line:
				c = f.next()
				self.teorijska_nastava = c
				#self.teorijska_nastava = line[19:]
				print 'Teorijska nastava: '+'-'+self.teorijska_nastava+'-'
			if 'Praktična nastava' in line: #and line[20] not in ['0','1','2','3','4','5','6','7','8','9']:
				d = f.next()
				self.prakticna_nastava = d
				#self.prakticna_nastava = line[20:]
				print 'Prakticna nastava: '+'-'+self.prakticna_nastava+'-'
			if 'Literatura' in line:
				for i in range(7):
					a = f.next()
					if 'Broj časova' not in a:
						#self.literatura = line[11:]
						self.literatura += a
					else:
						break
				print 'Literatura: '+'-'+self.literatura+'-'
				
	def zameni(self):
		f1 = open('TEMPLATE.html', 'r') 
		f2 = open(self.ime_fajla, 'w') 
		
		replacements = {'-studijski-program-':self.studijski_program, '-predmet-':self.naziv_predmeta, '-nastavnik-':self.nastavnik, '-status-predmeta-':self.status_predmeta,
						'-espb-':self.espb, '-uslov-':self.uslov, '-opis-predmeta-':self.opis_predmeta, 
						'-teorijska-nastava-':self.teorijska_nastava, '-prakticna-nastava-':self.prakticna_nastava, 
						'-literatura-':self.literatura}

		for line in f1:
			for src, target in replacements.iteritems():
				line = line.replace(src, target)
			f2.write(line)
			
		f1.close()
		f2.close()
		
projekat = Projekat()

projekat.doc_txt_catdoc('/home/m/projekti/megatrend/das/T.5.2.Mikrokontroleri.doc') # sys.argv[1])# #
projekat.cir_u_lat()
projekat.izdvoj()
projekat.zameni()

