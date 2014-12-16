openCC -I. ../../similarityMeasures/dtw/dtw.c ../../basicDSPFuncs/basicDSPCFuncs.c ../../similarityMeasures/dtw/tables.c TSATables.cpp TSApool.cpp TSAsimilarity.cpp TSAdataIO.cpp searchPatternsAllDBQuery.cpp TSAlogs.cpp -o searchPatternsAllDBQuery_O3 -lm  -Ofast -ipa -LNO:prefetch=2:pf2=0 -CG:use_prefetchnta=on -LNO:prefetch_ahead=4 -LNO:simd=3 -align64  -OPT:align_unsafe=ON -msse2  -LNO:psimd_iso_unroll=ON -LNO:if_select_conv=1 -LNO:trip_count=90 -ffast-stdlib