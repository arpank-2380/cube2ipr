"""
cube2ipr.py code calculates inverse participation ratio (IPR)
for a series of cube files produced by Qbox, Gaussian, Espresso etc.
"""
import sys, re 
import copy
import glob
import numpy as np

class cube_data:
      """
         This includes methods to read cube files and perform a set of
         operations on them, e.g., squaring, integrating a cube file
      """

      def __init__(self,fname=None):
          if fname is not None:
             try:
                self.read_cube_file(fname)
             except IOError as e:
                print( "File used as input: %s" % fname )
                print( "File error ({0}): {1}".format(e.errno, e.strerror))
                exit()
          else:
             print("cube_data class cannot be initiated without a file name.")
             exit()
          #print(self.data)
          self.integral = self.cube_integrate()
          self.ipr = self.calc_ipr()

      def calc_ipr(self):
          """
             Calculates inverse participation ratio (IPR) 
          """
          square_integral,square = self.power_cube(power=2)
          power4_integral,power4 = self.power_cube(power=4)
          ipr = power4_integral/square_integral           
          return ipr
      
      def read_cube_file(self,fname):
          """
            Method to read cube file.
            Arg: fname => filename
          """
      
          infil = open(fname, 'r')
          for iline in range(0,2):
              infil.readline()
          info = infil.readline().split() # information regarding no of atoms and origins
          self.natom = int(info[0]) #Number of Atoms
          self.origin = np.array([float(info[1]),float(info[2]),float(info[3])]) #Position of Origin
          self.na = np.zeros(3,np.int32)            ### number ov voxels along lattice direction a[0],a[1] and a[2]
          self.a = np.zeros((3,3),np.float64)       ### lattice vectors
          lattice_vec = 0
          for iline in range(3,6):
              voxel_info = infil.readline().split() 
              self.na[lattice_vec] = int(voxel_info[0])
              self.a[lattice_vec,:] = float(voxel_info[1]),float(voxel_info[2]),float(voxel_info[3])
              lattice_vec += 1
          self.atoms = []
          self.coord = np.zeros((self.natom,3),np.float64)
          for atom in range(self.natom):
              atom_info = infil.readline().split()
              self.atoms.append(atom_info[0])
              self.coord[atom,:] = float(atom_info[2]), float(atom_info[3]), float(atom_info[4])

          self.data = np.zeros((self.na[0],self.na[1],self.na[2]),np.float64)
          ivoxel = 0
          for line in infil:
              for value in line.split():
                  self.data[ivoxel//(self.na[1]*self.na[2]), (ivoxel//self.na[2])%self.na[1], ivoxel%self.na[2]] = float(value)
                  ivoxel += 1  
          return None



      def power_cube(self,power=2,integrate=True):

          """
             Function to raise cube data to a power. Squares cube data by default.
             And to integrate the new data
          """
          power=self.data**power
          if integrate:
             integral = self.cube_integrate(power)
             return integral, power
          else:
             return power          


      def cube_integrate(self,data=None):
          """
           Integrate the entire cube data.
          """
          if data is None:
             data = self.data
          vol=np.linalg.det(self.a)
          density=np.sum(data)
          integral=vol*density
          return integral


def main():
    #cubedata = cube_data(fname='../penta/wf66-frame-0.cube')
    #print(cubedata.integral)
    #print(cubedata.calc_ipr())
    if (len(sys.argv) < 2 ) | (len(sys.argv) > 3):
       sys.exit("\033[91mNo cube file given as input. \nUsage: cube2ipr.py file.cube OR cube2ipr.py -prefix file_prefix (w/o .cube) \033[00m")

    print("------------------------------------------------------------------------")
    print("                             Cube2IPR                                   ")
    print("Converts a bunch of wave functions to Inverse Participation ratios (IPR)")
    print("                     Written by Arpan Kundu                             ")
    print("------------------------------------------------------------------------")
    
    if len(sys.argv) == 2:
       cubefile = sys.argv[1] 
       cubedata = cube_data(fname=cubefile)
       print("IPR = %12.4f"%cubedata.ipr)
    else:
       prefix = sys.argv[2]
       cube_file_list = sorted(glob.iglob(prefix+"*.cube"), key=lambda n: int(re.findall(r'\d+', n)[-1]))
       outfn = prefix+"_ipr.dat"
       outfile = open(outfn,"w+")
       outfile.write("#======================================================================================\n")
       outfile.write("#                                Generated by Cube2IPR                                 \n")
       outfile.write("#A script that converts a bunch of wave functions to Inverse Participation ratios (IPR)\n")
       outfile.write("#                               Written by Arpan Kundu                                 \n")
       outfile.write("#--------------------------------------------------------------------------------------\n")
       outfile.write("#          Column-1 ==> File name   and column-2 ==> IPR (unitless)                    \n")
       outfile.write("#======================================================================================\n")

       for cubefile in cube_file_list:
           cubedata = cube_data(fname=cubefile)
           outfile.write(" %s    %12.4f\n"%(cubefile,cubedata.ipr))
       print("IPR data is written in file: %s"%outfn)
     
    print("-----------------------------------------------------------------------")
    print("                        Cube2IPR FINISHED                              ")
    print("-----------------------------------------------------------------------")

if __name__ == "__main__":
     main()

