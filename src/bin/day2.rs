use intcode::*;

fn main() {
    let baseprogram: Vec<usize> = read_input_file("input2.txt");
    let target: usize = 19690720usize;

    for i in 0..100 {
        for j in 0..100 {
            let mut program = baseprogram.clone();
            program[1] = i;
            program[2] = j;
            let mut computer: Computer = Computer::new(program);
            let val = computer.run();

            if val == target {
                println!("{}", i * 100 + j);
                return ();
            }
        }
    }
}
