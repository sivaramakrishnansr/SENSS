cmd_cli_vt100.o = gcc -Wp,-MD,./.cli_vt100.o.d.tmp  -m64 -pthread  -march=native -DRTE_MACHINE_CPUFLAG_SSE -DRTE_MACHINE_CPUFLAG_SSE2 -DRTE_MACHINE_CPUFLAG_SSE3 -DRTE_MACHINE_CPUFLAG_SSSE3 -DRTE_MACHINE_CPUFLAG_SSE4_1 -DRTE_MACHINE_CPUFLAG_SSE4_2 -DRTE_MACHINE_CPUFLAG_AES -DRTE_MACHINE_CPUFLAG_PCLMULQDQ -DRTE_MACHINE_CPUFLAG_AVX -DRTE_MACHINE_CPUFLAG_RDRAND -DRTE_MACHINE_CPUFLAG_FSGSBASE -DRTE_MACHINE_CPUFLAG_F16C  -I/proj/SENSS/SENSS_git/SENSS/Setup/Netronome/pktgen-3.4.5/lib/cli/cli/x86_64-native-linuxapp-gcc/include -I/opt/netronome/srcpkg/dpdk-ns/x86_64-native-linuxapp-gcc/include -include /opt/netronome/srcpkg/dpdk-ns/x86_64-native-linuxapp-gcc/include/rte_config.h -O3 -D_GNU_SOURCE -W -Wall -Wstrict-prototypes -Wmissing-prototypes -Wmissing-declarations -Wold-style-definition -Wpointer-arith -Wcast-align -Wnested-externs -Wcast-qual -Wformat-nonliteral -Wformat-security -Wundef -Wwrite-strings -I/proj/SENSS/SENSS_git/SENSS/Setup/Netronome/pktgen-3.4.5/lib/cli -DRTE_CLI_HOST_COMMANDS -DRTE_LIBRTE_LUA -DCLI_STANDALONE -I/proj/SENSS/SENSS_git/SENSS/Setup/Netronome/pktgen-3.4.5/lib/cli/../lua/src -D_GNU_SOURCE   -fPIC -o cli_vt100.o -c /proj/SENSS/SENSS_git/SENSS/Setup/Netronome/pktgen-3.4.5/lib/cli/cli_vt100.c 
