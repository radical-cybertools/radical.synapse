all:
	@echo "create libext.a"
	cc -O0 -c -o atom_compute_extlib.o -fPIC compute_kernels.c
	ar rcs libext.a atom_compute_extlib.o
