import os
from modules.transpiler import transpiler

# for root, dirs, filenames in os.walk("src"):
#     print(root, dirs, filenames)


#     for dir1 in dirs:
#         print(dir1)

#     for filename in filenames:
#         if filename.endswith(".sea") or filename.endswith(".hea"):
#             transpiler.transpile(f"filename")

transpiler.transpile("src/test1.sea")
