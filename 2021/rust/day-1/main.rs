use std::fs;

fn main() {
    let input = fs::read_to_string("input")
        .expect("Something went wrong reading the file");
    let input: Vec<i32> = input.trim().split("\n").map(|e| e.parse().expect("fail!")).collect();

    let mut count = 0;
    let mut last = -1;

    for n in &input {
        if last > 0 && *n > last {
            count += 1;
        }
        last = *n;
    }

    println!("{}", count);

    count = 0;
    last = -1;

    for i in 3..input.len() {
        let sum = &input[i-3..i].iter().fold(0, |a, b| a + b);
        if *sum > last {
            count += 1;
        }
        last = *sum
    }

    println!("{}", count);
}
