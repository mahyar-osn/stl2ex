Download the package:

`git clone https://github.com/mahyar-osn/stl2ex.git`

Go to the `stl2ex` directory and run:
`pip install -r requirements.txt`

Convert your `stl` file to `ex` by doing:

`python stl2ex.py <path_to_stl_file> --output-ex <path_to_ex_file>`

Please do not include the ex extension to the output file. If you need to reduce the data size, run the code by:

`python stl2ex.py <path_to_stl_file> --output-ex <path_to_ex_file> --downsampling-factor <any_number>`

Example, if `<any_number>` == 10, then the ex data will be 10X smaller than the original stl file.