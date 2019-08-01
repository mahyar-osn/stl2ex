import numpy
import operator
from stl import mesh

my_mesh = mesh.Mesh.from_file('C:\\Users\\mosa004\\Desktop\\temp\\Hooman\\16_0067_tibia_l_PLSR_prediction.stl')

felem = open('LumbarSpinePhantom.exelem', 'w')
# print header to output files
value = " Group name: convert_from_stl"
s = str(value)
felem.write(s)
felem.write('\n Shape.  Dimension=2\n')
felem.write(' #Scale factor sets= 1\n')
felem.write('   l.Lagrange, #Scale factors= 4\n')
felem.write(' #Nodes=4\n')
felem.write(' #Fields=1\n')
felem.write(' 1) coordinates, coordinate, rectangular cartesian, #Components=3\n')
felem.write('   x.  l.Lagrange*l.Lagrange, no modify, standard node based.\n')
felem.write('     #Nodes= 4\n')
felem.write('      1.  #Values=1\n')
felem.write('       Value indices:     1\n')
felem.write('       Scale factor indices:   1\n')
felem.write('      2.  #Values=1\n')
felem.write('       Value indices:     1\n')
felem.write('       Scale factor indices:   2\n')
felem.write('      3.  #Values=1\n')
felem.write('       Value indices:     1\n')
felem.write('       Scale factor indices:   3\n')
felem.write('      4.  #Values=1\n')
felem.write('       Value indices:     1\n')
felem.write('       Scale factor indices:   4\n')
felem.write('   y.  l.Lagrange*l.Lagrange, no modify, standard node based.\n')
felem.write('     #Nodes= 4\n')
felem.write('      1.  #Values=1\n')
felem.write('       Value indices:     1\n')
felem.write('       Scale factor indices:   1\n')
felem.write('      2.  #Values=1\n')
felem.write('       Value indices:     1\n')
felem.write('       Scale factor indices:   2\n')
felem.write('      3.  #Values=1\n')
felem.write('       Value indices:     1\n')
felem.write('       Scale factor indices:   3\n')
felem.write('      4.  #Values=1\n')
felem.write('       Value indices:     1\n')
felem.write('       Scale factor indices:   4\n')
felem.write('   z.  l.Lagrange*l.Lagrange, no modify, standard node based.\n')
felem.write('     #Nodes= 4\n')
felem.write('      1.  #Values=1\n')
felem.write('       Value indices:     1\n')
felem.write('       Scale factor indices:   1\n')
felem.write('      2.  #Values=1\n')
felem.write('       Value indices:     1\n')
felem.write('       Scale factor indices:   2\n')
felem.write('      3.  #Values=1\n')
felem.write('       Value indices:     1\n')
felem.write('       Scale factor indices:   3\n')
felem.write('      4.  #Values=1\n')
felem.write('       Value indices:     1\n')
felem.write('       Scale factor indices:   4\n')


facet_count = 0 # count the number of facets
node_count = 0  # count the number of nodes

coord_hash ={'0_0_0': 0};

for p in my_mesh.points:

# for the first vertex coordinates
    x = my_mesh.v0[facet_count][0]
    y = my_mesh.v0[facet_count][1]
    z = my_mesh.v0[facet_count][2]

    coord_string = str(x)+'_'+str(y)+'_'+str(z)
    if(coord_string in coord_hash):
        node0 = coord_hash[coord_string]
    else:
        node_count += 1
        coord_hash[coord_string] = node_count
        node0 = node_count

# for the second vertex coordinates
    x = my_mesh.v1[facet_count][0]
    y = my_mesh.v1[facet_count][1]
    z = my_mesh.v1[facet_count][2]

    coord_string = str(x)+'_'+str(y)+'_'+str(z)
    if(coord_string in coord_hash):
        node1 = coord_hash[coord_string];
    else:
        node_count += 1;
        coord_hash[coord_string] = node_count;
        node1 = node_count;

# for the third vertex coordinates
    x = my_mesh.v2[facet_count][0]
    y = my_mesh.v2[facet_count][1]
    z = my_mesh.v2[facet_count][2]

    coord_string = str(x)+'_'+str(y)+'_'+str(z)
    if(coord_string in coord_hash):
        node2 = coord_hash[coord_string];
    else:
        node_count += 1;
        coord_hash[coord_string] = node_count;
        node2 = node_count;

    facet_count += 1

# print the facet/element to file
    felem.write(" Element: " + str(facet_count) + " 0 0 " + '\n')
    felem.write("   Nodes:\n")
    felem.write("        " + str(node0) + "   " +  str(node1) + "   " +  str(node2) + "   " +  str(node2) + '\n')
    felem.write("   Scale factors:\n")
    felem.write("        1.000   1.000   1.000   1.000 \n")

felem.close

fnode = open('LumbarSpinePhantom.exnode', 'w')
fnode.write(s)
fnode.write('\n #Fields= 1\n')
fnode.write(' 1) coordinates, coordinate, rectangular cartesian, #Components=3\n')
fnode.write('   x.  Value index= 1, #Derivatives=0\n')
fnode.write('   y.  Value index= 2, #Derivatives=0\n')
fnode.write('   z.  Value index= 3, #Derivatives=0\n')

for key in coord_hash:
    node = coord_hash[key];
    if node != 0:
        fnode.write(" Node: " + str(node) + '\n')
        x, y, z = key.split("_")
        fnode.write(" " + str(x) + " " + str(y) + " " + str(z) + '\n')

fnode.close
