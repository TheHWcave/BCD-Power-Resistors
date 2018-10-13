
from collections import namedtuple
import itertools
# 1 calculate possible combination of 4 resistors in parallel and serial connection
#   assuming all resistors have the same power rating
# 2 determine which resistor will bear the highest load 
# 3 find how much the overall circuit can be loaded above the rating of a single resistor without
#   overloading the resistor found in step 2

Record = namedtuple('Record','Rtotal Overload Stress Rmax Circuit Method')
Records = []
Results = []
   


def RowPar_ColSer(Circ): 
	# calculate circuit resistance going parallel rows and then serial for columns
	# then find total watts and resistor with highest watt
	# insert into Comb list if a unique new entry based on total resistance and overload potential
	Rr = [0,0,0,0]
	Rt = 0.0
	for r in range(0,4):
		R = 0.0
		for c in range(0,4):
			if Circ[r][c] > 0:
				R = R + 1.0/Circ[r][c]
		if R > 0:
			R = 1.0/R
		Rr[r] = R
		Rt = Rt + R
	if Rt > 0:
		# calculate total wattage based on 1A current
		Wt = Rt # total Watt = Rt * I*I  
		Vt = Rt # total voltage is Rt * I 
		Wm = 0.0
		for r in range(0,4):
			Vr = Rr[r]   # voltage at each series resistor = Rr * I     
			for c in range(0,4):
				Rx = Circ[r][c]
				if Rx > 0:
					Wx = (Vr*Vr)/Rx   # power at resistor is U*U/R
					if Wx > Wm:
						Wm = Wx
						Rm = Rx
		Duplicate = False
		for Rec in Records:
			if (round(Rec.Rtotal,4) == round(Rt,4)) and (round(Rec.Overload,4) == round(Wt/Wm,4)):
				Duplicate = True
				break
		if not Duplicate:
			Entry = Record(Rtotal=Rt,Overload=Wt/Wm,Stress=Wm/Wt,Rmax=Rm,Circuit=Circ,Method=1)
			Records.append(Entry)
	return

def ColSer_RowPar(Circ): 
	# calculate circuit resistance going serial for columns and then parallel for rows
	# then find total watts and resistor with highest watt
	# insert into Comb list if a unique new entry based on total resistance and overload potential
	Rc = [0,0,0,0]
	Rt = 0.0
	for c in range(0,4):
		R = 0.0
		for r in range(0,4):
			if Circ[r][c] > 0:
				R = R + Circ[r][c]
		Rc[c] = R
		if R > 0:
			Rt = Rt + 1.0/R
	if Rt > 0:
		Rt = 1.0/Rt
	if Rt > 0:
		# calculate total wattage based on 1A
		Wt = Rt # total Watt = Rt * I*I 
		Vt = Rt # total voltage is Rt * I 
		Wm = 0.0
		for c in range(0,4):
			if Rc[c] > 0:
				Ic = Vt / Rc[c] # current in the column
				for r in range(0,4):
					Rx = Circ[r][c]
					if Rx > 0:
						Wx = (Ic*Ic)*Rx
						if Wx > Wm:
							Wm = Wx
							Rm = Rx
		Duplicate = False
		for Rec in Records:
			if (round(Rec.Rtotal,4) == round(Rt,4)) and (round(Rec.Overload,4) == round(Wt/Wm,4)):
				Duplicate = True
				break
		if not Duplicate:
			Entry = Record(Rtotal=Rt,Overload=Wt/Wm,Stress=Wm/Wt,Rmax=Rm,Circuit=Circ,Method=2)
			Records.append(Entry)
	return

def Do_DoubleSys(R,Thi,Tlo,Sone,Sten,M):
	Duplicate = False
	for Res in Results:
		if round(Res.Rtotal,4) == round(R,4):
			Duplicate = True
			break
	if not Duplicate:
		Target = int(10*round(R,4))/10.0
		if Target > Thi: Thi = Target
		if Target < Tlo: Tlo = Target 
		Delta = abs(Target - R)
		Err = Delta/Target
		Entry = DoubleSys(Rtarget=Target,Rtotal=R,Delta=Delta,Err=Err,SysOne=Sone,SysTen=Sten,Method=M)
		Results.append(Entry)
	return (Thi,Tlo)
	
def Circuit_2_String(Rec):
	Pretty =''
	Circuit = Rec.Circuit
	first = True
	if Rec.Method == 1:
		# pretty print config 1 - resistors in same row are parallel, rows are connected in series
		for r in range(0,4):
			p = 0
			paren = 0
			for c in range(0,4):
				R = Circuit[r][c]
				if R > 0:
					p = p + 1
			if p > 0:
				if first:
					first = False
				else:
					Pretty = Pretty + '+'
			if (p > 1): 
				paren = 1
			for c in range(0,4):
				R = Circuit[r][c] 
				if R > 0:
					if paren == 1:
						Pretty = Pretty +'('
						paren = 2
					Pretty = Pretty +str(R)
					p = p -1
					if p > 0:
						Pretty = Pretty + '|'
			if paren == 2:
				Pretty = Pretty + ')'
	else:
		# pretty print config 2 - resistors in same column are serial, columns are connected in parallel
		for c in range(0,4):
			p = 0
			paren = 0
			for r in range(0,4):
				R = Circuit[r][c]
				if R > 0:
					p = p + 1
			if p > 0:
				if first:
					first = False
				else:
					Pretty = Pretty + '|'
			if (p > 1): 
				paren = 1
			for r in range(0,4):
				R = Circuit[r][c] 
				if R > 0:
					if paren == 1:
						Pretty = Pretty + '('
						paren = 2
					Pretty = Pretty + str(R)
					p = p -1
					if p > 0:
						Pretty = Pretty + '+'
			if paren == 2:
				Pretty = Pretty + ')'
	return(Pretty)

Res = (1,2,4,8)
print('Resistors: ',Res)
for Nres in range(1,5):
	for Comb in itertools.combinations(Res,Nres):
		#   1     2       3        4
		#   1    1 2    1 2 4    1 2 3 4
		#   2    1 4    1 2 8
		#   4    1 8    1 4 8
		#   8    2 4    2 4 8
		#        2 8
		#        4 8
		Circuit = [[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]]
		if Nres == 1:
			Circuit[0][0] = Comb[0]
			RowPar_ColSer(Circuit)
			ColSer_RowPar(Circuit) 
		else:
			if Nres == 2:
				Max = 16
				Mask = 1
				SR = 1
			elif Nres == 3:
				Max = 4096  # 3 resistors with 4 bits = 12
				Mask = 3
				SR = 2
			else:
				Max = 65536  # 4 resistors with 4 bits = 16
				Mask = 3
				SR = 2
			for n in range(0,Max):
				p = n
				Circuit = [[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]]
				for x in range(0,Nres):
					c = p & Mask
					p = p >> SR
					r = p & Mask
					p = p >> SR
					Circuit[c][r] = Comb[x]
				RowPar_ColSer(Circuit)
				ColSer_RowPar(Circuit) 
#----------------------------------------------------------------------
# sort list by total resistor and pretty-print
Records.sort()
n = 0
for Rec in Records: 
	Pretty = Circuit_2_String(Rec)
	n = n + 1
	print('{:8.4f} Ohm using {:^16s}, most stressed R={:1d} at {:4.0f}%, possible overload {:5.1f}%'.format(Rec[0],Pretty,Rec[3],100*Rec[2],100*Rec[1]))
print(str(n)+ ' records ')
	
Rone = Records
Records = []

Res = (10,20,40,80)
print('Resistors: ',Res)
for Nres in range(1,5):
	for Comb in itertools.combinations(Res,Nres):
		#   1     2       3        4
		#   1    1 2    1 2 4    1 2 3 4
		#   2    1 4    1 2 8
		#   4    1 8    1 4 8
		#   8    2 4    2 4 8
		#        2 8
		#        4 8
		Circuit = [[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]]
		if Nres == 1:
			Circuit[0][0] = Comb[0]
			RowPar_ColSer(Circuit)
			ColSer_RowPar(Circuit) 
		else:
			if Nres == 2:
				Max = 16
				Mask = 1
				SR = 1
			elif Nres == 3:
				Max = 4096  # 3 resistors with 4 bits = 12
				Mask = 3
				SR = 2
			else:
				Max = 65536  # 4 resistors with 4 bits = 16
				Mask = 3
				SR = 2
			for n in range(0,Max):
				p = n
				Circuit = [[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]]
				for x in range(0,Nres):
					c = p & Mask
					p = p >> SR
					r = p & Mask
					p = p >> SR
					Circuit[c][r] = Comb[x]
				RowPar_ColSer(Circuit)
				ColSer_RowPar(Circuit) 
#----------------------------------------------------------------------
# sort list by total resistor and pretty-print
Records.sort()
n = 0
for Rec in Records: 
	Pretty = Circuit_2_String(Rec)
	n = n + 1
	print('{:8.4f} Ohm using {:^16s}, most stressed R={:1d} at {:4.0f}%, possible overload {:5.1f}%'.format(Rec[0],Pretty,Rec[3],100*Rec[2],100*Rec[1]))
print(str(n)+ ' records ')
Rten = Records

Results = []
DoubleSys = namedtuple('DoubleSys','Rtarget Rtotal Delta Err SysOne SysTen Method')
Tlo = 9.9E9
Thi = -9.9E9
for RecOne in Rone:
	R = RecOne.Rtotal
	(Thi,Tlo) = Do_DoubleSys(R,Thi,Tlo,RecOne,[],0)
for RecTen in Rten:
	R = RecTen.Rtotal
	(Thi,Tlo) = Do_DoubleSys(R,Thi,Tlo,[],RecTen,0)

for RecOne in Rone:
	for RecTen in Rten:
		
		R = RecOne.Rtotal + RecTen.Rtotal 
		(Thi,Tlo) = Do_DoubleSys(R,Thi,Tlo,RecOne,RecTen,1)
		

		R = 1.0/((1.0/RecOne.Rtotal) + (1.0/RecTen.Rtotal))
		(Thi,Tlo) = Do_DoubleSys(R,Thi,Tlo,RecOne,RecTen,2)

Results.sort()

n = 0
for T in range(int(10*Tlo),int(10*Thi)+1):
	Best = []
	MinErr   = 9.9E9
	for Res in Results:
		if int(10*Res.Rtarget) == T:
			if Res.Err < MinErr: 
				Best = Res
				MinErr = Res.Err
		if int(10*Res.Rtarget) > T: 
			break
	if Best != []:
		if Best.Err < 0.05:
			n = n + 1
			print('{:5.1f} Ohm with {:3.2f}% error {:8.4f} using'.format(Best.Rtarget, 100*Best.Err,Best.Rtotal),end='')
			if Best.Method > 0:
				if Best.Method == 1:
					Pretty = ' '+Circuit_2_String(Best.SysOne)+'  +  '+Circuit_2_String(Best.SysTen)+' '
					NumStr = '{:7.4f} + {:7.4f}'.format(Best.SysOne.Rtotal,Best.SysTen.Rtotal)
				else:
					Pretty = ' '+Circuit_2_String(Best.SysOne)+'  |  '+Circuit_2_String(Best.SysTen)+' '
					NumStr = '{:7.4f} | {:7.4f}'.format(Best.SysOne.Rtotal,Best.SysTen.Rtotal)
			else:
				if Best.SysOne == []:
					Pretty = Circuit_2_String(Best.SysTen)
					NumStr = '{:7.4f}'.format(Best.SysTen.Rtotal)
				else:
					Pretty = Circuit_2_String(Best.SysOne)
					NumStr = '{:7.4f}'.format(Best.SysOne.Rtotal)
			print('{:^32s} {:^13s}'.format(Pretty,NumStr))
		#else:
			#print('{:5.1f} Ohm ---'.format(Best.Rtarget))
	#else:
		#print('{:5.1f} Ohm ---'.format(T/10.0))
print(str(n)+ ' records ')
