/*
 * Fast RNG for the hierarchical TM demo.
 *
 * The PCG32 implementation is taken from CAIR TMU (same file layout as
 * tmu/lib/src/random/pcg32_fast.c in https://github.com/cair/tmu).
 *
 * XOR-shift 128+ is also from that tree (tmu/lib/src/random/xorshift128.c).
 * TMU's Python ClauseBank seeds both generators; we match that. Timed runs
 * on this workload were slightly faster with PCG32 than with 128+ alone,
 * so tm_rng_uniform01() uses PCG32 only.
 */

#include <stdint.h>

#include "TsetlinMachine.h"

/* ---- PCG32 (from TMU) ---- */

static uint64_t const pcg32_multiplier = 6364136223846793005u;
static uint64_t pcg32_state = 0xcafef00dd15ea5e5u;

static void pcg32_seed_local(uint64_t seed)
{
	pcg32_state = seed;
}

static uint32_t pcg32_draw(void)
{
	uint64_t x = pcg32_state;
	unsigned int count = (unsigned int)(x >> 61);
	pcg32_state = x * pcg32_multiplier;
	return (uint32_t)((x ^ x >> 22) >> (22 + count));
}

/* ---- xorshift128+ (from TMU; seeded for parity, not used for floats) ---- */

static uint64_t xs128_state[2] = {0xcafef00dbadc0ffeULL, 0xdeadbeef12345678ULL};

static void xorshift128p_seed_local(uint64_t seed)
{
	xs128_state[0] = seed;
	xs128_state[1] = ~seed;
}

void tm_rng_seed(uint64_t seed)
{
	uint64_t s = seed ? seed : 1ULL;

	pcg32_seed_local(s);
	xorshift128p_seed_local(s);
}

double tm_rng_uniform01(void)
{
	return (double)pcg32_draw() / (double)UINT32_MAX;
}
