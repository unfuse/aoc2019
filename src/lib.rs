// IntCode library for AOC 2019
use std::fs;

pub struct Computer {
    program: Vec<usize>,
    cursor: usize,
}

impl Computer {
    pub fn new(program: Vec<usize>) -> Computer {
        Computer { program, cursor: 0 }
    }

    pub fn run(&mut self) -> usize {
        // println!("Program is {:?}", self.program);
        // println!("Cursor at {}", self.cursor);

        loop {
            match self.step() {
                ReturnCode::TERMINATE => break,
                _ => continue,
            };
        }

        self.program[0]
    }

    fn step(&mut self) -> ReturnCode {
        let opcode: usize = self.program[self.cursor];

        match opcode {
            1 => {
                let src1: usize = self.program[self.cursor + 1];
                let src2: usize = self.program[self.cursor + 2];
                let dest: usize = self.program[self.cursor + 3];

                self.program[dest] = self.program[src1] + self.program[src2];
                self.cursor += 4;
                ReturnCode::CONTINUE
            }
            2 => {
                let src1: usize = self.program[self.cursor + 1];
                let src2: usize = self.program[self.cursor + 2];
                let dest: usize = self.program[self.cursor + 3];

                self.program[dest] = self.program[src1] * self.program[src2];
                self.cursor += 4;
                ReturnCode::CONTINUE
            }
            99 => {
                self.cursor += 1;
                ReturnCode::TERMINATE
            }
            a => panic!(format!("Encountered invalid opcode {}", a)),
        }
    }
}

pub enum ReturnCode {
    HALT,
    CONTINUE,
    TERMINATE,
}

pub fn read_input_file(file: &str) -> Vec<usize> {
    let program: Vec<usize> = fs::read_to_string(file)
        .expect(&format!("Could not read file {}", file)[..])
        .split(",")
        .map(|s| -> usize { s.parse::<usize>().unwrap() })
        .collect();

    return program;
}
