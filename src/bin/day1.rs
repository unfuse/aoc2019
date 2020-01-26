use std::fs;

fn main() {
    let input: String = fs::read_to_string("input1.txt").expect("Couldn't open file");
    let total = input
        .lines()
        .map(|s| -> i32 { s.parse::<i32>().unwrap() })
        .fold(0, |acc, elt| acc + fuel_rec(elt));

    println!("{}", total);
}

fn fuel(mass: i32) -> i32 {
    (mass / 3) - 2
}

fn fuel_rec(mass: i32) -> i32 {
    let f: i32 = fuel(mass);

    if f < 0 {
        return 0;
    }

    f + fuel_rec(f)
}
