import os
import sys
import argparse

from stl import mesh


VALUE = " Group name: convert_from_stl"


class ProgramArguments(object):

    def __init__(self):
        self.input_stl = None
        self.output_ex = None
        self.downsampling_factor = None


def _write_elem_headings(file_name):
    with open(file_name, "w") as felem:
        felem.write(VALUE)
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

    return


def _write_elem(file_name, node_list, facet):

    node0, node1, node2 = node_list

    with open(file_name, "a") as felem:
        felem.write(" Element: " + str(facet) + " 0 0 " + '\n')
        felem.write("   Nodes:\n")
        felem.write("        " + str(node0) + "   " + str(node1) + "   " + str(node2) + "   " + str(node2) + '\n')
        felem.write("   Scale factors:\n")
        felem.write("        1.000   1.000   1.000   1.000 \n")


def _write_node(file_name, coords, downsample=None):
    with open(file_name, 'w') as fnode:
        fnode.write(VALUE)
        fnode.write('\n #Fields= 1\n')
        fnode.write(' 1) coordinates, coordinate, rectangular cartesian, #Components=3\n')
        fnode.write('   x.  Value index= 1, #Derivatives=0\n')
        fnode.write('   y.  Value index= 2, #Derivatives=0\n')
        fnode.write('   z.  Value index= 3, #Derivatives=0\n')

        count = 0
        for key in coords:
            node = coords[key]
            if node != 0:
                if downsample:
                    if count % int(downsample) == 0:
                        fnode.write(" Node: " + str(node) + '\n')
                        x, y, z = key.split("_")
                        fnode.write(" " + str(x) + " " + str(y) + " " + str(z) + '\n')
                else:
                    fnode.write(" Node: " + str(node) + '\n')
                    x, y, z = key.split("_")
                    fnode.write(" " + str(x) + " " + str(y) + " " + str(z) + '\n')
            count += 1

    return


def convert_stl_to_ex(stl_file, node_file_name=None, elem_file_name=None, ds=None):
    my_mesh = mesh.Mesh.from_file(stl_file)

    # TODO: bug fix - invalid element scale factor in CMGUI
    # _write_elem_headings(elem_file_name)

    facet_count = 0  # count the number of facets
    node_count = 0  # count the number of nodes

    coord_hash = {'0_0_0': 0}

    for _ in my_mesh.points:

        # for the first vertex coordinates
        x = my_mesh.v0[facet_count][0]
        y = my_mesh.v0[facet_count][1]
        z = my_mesh.v0[facet_count][2]

        coord_string = str(x) + '_' + str(y) + '_' + str(z)
        if coord_string in coord_hash:
            node0 = coord_hash[coord_string]
        else:
            node_count += 1
            coord_hash[coord_string] = node_count
            node0 = node_count

        # for the second vertex coordinates
        x = my_mesh.v1[facet_count][0]
        y = my_mesh.v1[facet_count][1]
        z = my_mesh.v1[facet_count][2]

        coord_string = str(x) + '_' + str(y) + '_' + str(z)
        if coord_string in coord_hash:
            node1 = coord_hash[coord_string]
        else:
            node_count += 1
            coord_hash[coord_string] = node_count
            node1 = node_count

        # for the third vertex coordinates
        x = my_mesh.v2[facet_count][0]
        y = my_mesh.v2[facet_count][1]
        z = my_mesh.v2[facet_count][2]

        coord_string = str(x) + '_' + str(y) + '_' + str(z)
        if coord_string in coord_hash:
            node2 = coord_hash[coord_string]
        else:
            node_count += 1
            coord_hash[coord_string] = node_count
            node2 = node_count

        facet_count += 1

        # TODO: bug fix - invalid element scale factor in CMGUI
        # _write_elem(elem_file_name, (node0, node1, node2), facet_count)

    _write_node(node_file_name, coord_hash, downsample=ds)


def main():
    args = parse_args()
    if os.path.exists(args.input_stl):
        if args.output_ex is None:
            output_exnode = args.input_stl + '.exnode'
            output_exelem = args.input_stl + '.exelem'
        else:
            output_exnode = args.output_ex + '.exnode'
            output_exelem = args.output_ex + '.exelem'

        if args.downsampling_factor:
            ds = args.downsampling_factor
        else:
            ds = None

        convert_stl_to_ex(args.input_stl, output_exnode, output_exelem, ds)
    else:
        sys.exit(-1)


def parse_args():
    parser = argparse.ArgumentParser(description="Transform Neurolucida Xml data file to ex format.")
    parser.add_argument("input_stl", help="Location of the input xml file.")
    parser.add_argument("--output-ex", help="Location of the output ex file. "
                                            "[defaults to the location of the input file if not set.]")
    parser.add_argument("--downsampling-factor", help="Downsampling factor to reduce data points.")

    program_arguments = ProgramArguments()
    parser.parse_args(namespace=program_arguments)

    return program_arguments


if __name__ == "__main__":
    main()
