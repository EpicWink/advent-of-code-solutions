#include <stdio.h>
#include <string.h>

struct Instruction {
    unsigned int opcode;
    unsigned int a;
    unsigned int b;
    unsigned int c;
};

void addr(struct Instruction instruction, long long state[6]) {
    state[instruction.c] = state[instruction.a] + state[instruction.b];
}

void addi(struct Instruction instruction, long long state[6]) {
    state[instruction.c] = state[instruction.a] + (long long) instruction.b;
}

void mulr(struct Instruction instruction, long long state[6]) {
    state[instruction.c] = state[instruction.a] * state[instruction.b];
}

void muli(struct Instruction instruction, long long state[6]) {
    state[instruction.c] = state[instruction.a] * (long long) instruction.b;
}

void banr(struct Instruction instruction, long long state[6]) {
    state[instruction.c] = state[instruction.a] & state[instruction.b];
}

void bani(struct Instruction instruction, long long state[6]) {
    state[instruction.c] = state[instruction.a] & (long long) instruction.b;
}

void borr(struct Instruction instruction, long long state[6]) {
    state[instruction.c] = state[instruction.a] | state[instruction.b];
}

void bori(struct Instruction instruction, long long state[6]) {
    state[instruction.c] = state[instruction.a] | (long long) instruction.b;
}

void setr(struct Instruction instruction, long long state[6]) {
    state[instruction.c] = state[instruction.a];
}

void seti(struct Instruction instruction, long long state[6]) {
    state[instruction.c] = instruction.a;
}

void gtir(struct Instruction instruction, long long state[6]) {
    state[instruction.c] = (long long) instruction.a > instruction.b;
}

void gtri(struct Instruction instruction, long long state[6]) {
    state[instruction.c] = (long long) state[instruction.a] > instruction.b;
}

void gtrr(struct Instruction instruction, long long state[6]) {
    state[instruction.c] = (long long) state[instruction.a] > state[instruction.b];
}

void eqir(struct Instruction instruction, long long state[6]) {
    state[instruction.c] = (long long) instruction.a == instruction.b;
}

void eqri(struct Instruction instruction, long long state[6]) {
    state[instruction.c] = (long long) state[instruction.a] == instruction.b;
}

void eqrr(struct Instruction instruction, long long state[6]) {
    state[instruction.c] = (long long) state[instruction.a] == state[instruction.b];
}

void apply(struct Instruction instruction, long long state[6]) {
    switch (instruction.opcode) {
        case 0: addr(instruction, state); break;
        case 1: addi(instruction, state); break;
        case 2: mulr(instruction, state); break;
        case 3: muli(instruction, state); break;
        case 4: banr(instruction, state); break;
        case 5: bani(instruction, state); break;
        case 6: borr(instruction, state); break;
        case 7: bori(instruction, state); break;
        case 8: setr(instruction, state); break;
        case 9: seti(instruction, state); break;
        case 10: gtir(instruction, state); break;
        case 11: gtri(instruction, state); break;
        case 12: gtrr(instruction, state); break;
        case 13: eqir(instruction, state); break;
        case 14: eqri(instruction, state); break;
        case 15: eqrr(instruction, state); break;
    }
}

unsigned int opcode2int(char* opcode) {
    if (strcmp(opcode, "addr") == 0) return 0;
    else if (strcmp(opcode, "addi") == 0) return 1;
    else if (strcmp(opcode, "mulr") == 0) return 2;
    else if (strcmp(opcode, "muli") == 0) return 3;
    else if (strcmp(opcode, "banr") == 0) return 4;
    else if (strcmp(opcode, "bani") == 0) return 5;
    else if (strcmp(opcode, "borr") == 0) return 6;
    else if (strcmp(opcode, "bori") == 0) return 7;
    else if (strcmp(opcode, "setr") == 0) return 8;
    else if (strcmp(opcode, "seti") == 0) return 9;
    else if (strcmp(opcode, "gtir") == 0) return 10;
    else if (strcmp(opcode, "gtri") == 0) return 11;
    else if (strcmp(opcode, "gtrr") == 0) return 12;
    else if (strcmp(opcode, "eqir") == 0) return 13;
    else if (strcmp(opcode, "eqri") == 0) return 14;
    else if (strcmp(opcode, "eqrr") == 0) return 15;
    else {
        printf("Bad opcode: %s\n", opcode);
        return -1;
    }
}


int main(int argc, char* argv[]) {
//    const struct Instruction instructions[36] = {
//        {1, 4, 16, 4},
//        {9, 1, 9, 3},
//        {9, 1, 6, 2},
//        {2, 3, 2, 5},
//        {15, 5, 1, 5},
//        {0, 5, 4, 4},
//        {1, 4, 1, 4},
//        {0, 3, 0, 0},
//        {1, 2, 1, 2},
//        {12, 2, 1, 5},
//        {0, 4, 5, 4},
//        {9, 2, 9, 4},
//        {1, 3, 1, 3},
//        {12, 3, 1, 5},
//        {0, 5, 4, 4},
//        {9, 1, 0, 4},
//        {2, 4, 4, 4},
//        {1, 1, 2, 1},
//        {2, 1, 1, 1},
//        {2, 4, 1, 1},
//        {3, 1, 11, 1},
//        {1, 5, 1, 5},
//        {2, 5, 4, 5},
//        {1, 5, 2, 5},
//        {0, 1, 5, 1},
//        {0, 4, 0, 4},
//        {9, 0, 1, 4},
//        {8, 4, 3, 5},
//        {2, 5, 4, 5},
//        {0, 4, 5, 5},
//        {2, 4, 5, 5},
//        {3, 5, 14, 5},
//        {2, 5, 4, 5},
//        {0, 1, 5, 1},
//        {9, 0, 6, 0},
//        {9, 0, 7, 4}};
//    const unsigned int instruction_pointer_register = 4;
//    const unsigned int n_instructions = 36;
    FILE *f;
    unsigned int instruction_pointer_register;
    struct Instruction instructions[64];
    unsigned int n_instructions = 0;
    char opcode_str[16];
    unsigned int opcode, a, b, c;

    long long state[6] = {0, 0, 0, 0, 0, 0};
    long long instruction_idx = 0;
//    long long state[6] = {42, 10551260, 3262642, 9392, 5, 0};  // step 792721200000 - 1
//    long long instruction_idx = 11;

    f = fopen(argv[1], "r");
    fscanf(f, "%*s %u\n", &instruction_pointer_register);
    while (1) {
        if (fscanf(f, "%s %u %u %u\n", opcode_str, &a, &b, &c) < 4) {
            break;
        }
        opcode = opcode2int(opcode_str);
        struct Instruction new_instruction = {opcode, a, b, c};
        instructions[n_instructions] = new_instruction;
        n_instructions += 1;
    }
    fclose(f);

    unsigned long long j = 0;
    while ((instruction_idx >= 0) && (instruction_idx < n_instructions)) {
        state[instruction_pointer_register] = instruction_idx;
        apply(instructions[instruction_idx], state);
        instruction_idx = state[instruction_pointer_register];
        instruction_idx += 1;

        if (j % 100000000 == 99999999) {
            printf(
                "Finished step %llu, state: (%lld, %lld, %lld, %lld, %lld, %lld)\n",
                j + 1, state[0], state[1], state[2], state[3], state[4], state[5]);
        }
        j += 1;
    }

    printf(
        "Program finished after %llu steps with state: (%lld, %lld, %lld, %lld, %lld, %lld)\n",
        j, state[0], state[1], state[2], state[3], state[4], state[5]);

    return 0;
}
