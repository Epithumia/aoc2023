use rdcl_aoc_helpers::input::WithReadLines;
use std::fs::File;

pub fn day1(path: &String) {
    println!("Jour 1");
    let data: Vec<String> = File::open(path).read_lines::<String>(1).collect();
    let mut p1: u32 = 0;
    let mut p2: u32 = 0;
    for row in data {
        let row1: String = row.chars().filter(|c| c.is_digit(10)).collect();
        let d = row1
            .chars()
            .take(1)
            .collect::<String>()
            .parse::<u32>()
            .unwrap()
            * 10;
        let u = row1
            .chars()
            .rev()
            .take(1)
            .collect::<String>()
            .parse::<u32>()
            .unwrap();
        p1 += d + u;
        let row1: String = row
            .replace("one", "one1one")
            .replace("two", "two2two")
            .replace("three", "three3three")
            .replace("four", "four4four")
            .replace("five", "five5five")
            .replace("six", "six6six")
            .replace("seven", "seven7seven")
            .replace("eight", "eight8eight")
            .replace("nine", "nine9nine")
            .chars()
            .filter(|c| c.is_digit(10))
            .collect();
        let d = row1
            .chars()
            .take(1)
            .collect::<String>()
            .parse::<u32>()
            .unwrap()
            * 10;
        let u = row1
            .chars()
            .rev()
            .take(1)
            .collect::<String>()
            .parse::<u32>()
            .unwrap();
        p2 += d + u;
    }
    println!("Partie 1 : {:?}", p1);
    println!("Partie 1 : {:?}", p2);
}
