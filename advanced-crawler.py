#!/usr/bin/env python3
import subprocess
import argparse
import os
from termcolor import colored
import random
import shutil
import time

def print_art():
    art = r'''

           ____                      ,
          /---.'.__             ____//
               '--.\           /.---'
          _______  \\         //
        /.------.\  \|      .'/  ______
       //  ___  \ \ ||/|\  //  _/_----.\__
      |/  /.-.\  \ \:|< >|// _/.'..\   '--'
         //   \'. | \'.|.'/ /_/ /  \\
        //     \ \_\/" ' ~\-'.-'    \\
       //       '-._| :R: |'-.__     \\
      //           (/'==='\)'-._\     ||
      ||                        \\    \|
      ||                         \\    '
      |/                          \\
                                   ||
                                   ||
                                   \\
 by-                                 
____   _  ____ _  _   _  _  _
| . \ / / |  _\||_|\ / / || |\
|  <_/_  ]| [ \| _ |/_  ]||/ /
|/\_/  |/ |___/|/ |/  |/ |__/

'''
    border = "|_| |_| |_| |_| |_| |_| |_| |_| |_| |_| |_| |_|"
    border2 = "X  X  X  X  X  X  X  X  X  X  X  X  X  X  X  X"

    colors = ["yellow", "blue", "magenta", "cyan", "green", "red"]
    art_color = random.choice(colors)
    remaining_colors = [color for color in colors if color != art_color]
    border_color = random.choice(remaining_colors)
    remaining_colors.remove(border_color)
    border2_color = random.choice(remaining_colors)

    print(colored(art, art_color, attrs=["bold"]))
    print(colored(border, border_color))
    print(colored(border2, border2_color))

def run_command(command):
    try:
        result = subprocess.run(
            command,
            shell=True,
            text=True,
            check=True,
            capture_output=True
        )
        return result.returncode
    except subprocess.CalledProcessError as e:
        print(colored(f"Error executing command: {command}", "red"))
        print(colored(f"Exit Code: {e.returncode}", "red"))
        if e.stdout:
            print(colored(f"--- STDOUT ---\n{e.stdout.strip()}", "yellow"))
        if e.stderr:
            print(colored(f"--- STDERR ---\n{e.stderr.strip()}", "red"))
        return e.returncode

assert shutil.which("waybackurls"), "waybackurls not installed or not in PATH"
assert shutil.which("gau"), "gau not installed or not in PATH"
assert shutil.which("hakrawler"), "hakrawler not installed or not in PATH"
assert shutil.which("github-endpoints"), "github-endpoints not installed or not in PATH"
assert shutil.which("cariddi"), "cariddi not installed or not in PATH"
assert shutil.which("gospider"), "gospider not installed or not in PATH"
assert shutil.which("katana"), "katana not installed or not in PATH"
assert shutil.which("gourlex"), "gourlex not installed or not in PATH"
assert shutil.which("urlfinder"), "urlfinder not installed or not in PATH"
assert shutil.which("anew"), "anew not installed or not in PATH"

def create_directories(directory_path):
    if not os.path.exists(directory_path):
        os.makedirs(directory_path)


def collect_urls(domain, output_folder):
    create_directories(output_folder)
    output_file = os.path.join(output_folder, f"{domain.replace('.', '_').replace('/', '_')}.txt")
    temp_output_file = f"{output_file}_temp"
    httpx_output_file = os.path.join(output_folder, f"{domain}_httpx.txt")

    if not os.path.exists(httpx_output_file):
        print(colored("Running httpx-toolkit on ", "blue") + colored(domain, "red", attrs=["bold"]))
        httpx_command = f"echo '{domain}' | httpx -silent | tee {httpx_output_file}"
        run_command(httpx_command)
    else:
        print(colored(f"Using cached httpx data for {domain}", "yellow", attrs=["bold"]))

    print(colored("Running waybackurls on ", "blue") + colored(domain, "red", attrs=["bold"]))
    command = f"echo {domain} | waybackurls | anew -q {temp_output_file}"
    assert run_command(command) == 0, "waybackurls command failed"
    count = int(subprocess.check_output(['wc', '-l', temp_output_file]).split()[0])
    print(colored(f"Found {count} URLs after wayback", "green", attrs=["bold"]))
    time.sleep(5)

    print(colored("Running gau on ", "blue") + colored(domain, "red", attrs=["bold"]))
    command = f"echo {domain} | gau | anew -q {temp_output_file}"
    assert run_command(command) == 0, "gau command failed"
    count = int(subprocess.check_output(['wc', '-l', temp_output_file]).split()[0])
    print(colored(f"Found {count} URLs after gau", "green", attrs=["bold"]))
    time.sleep(5)

    print(colored("Running hakrawler on ", "blue") + colored(domain, "red", attrs=["bold"]))
    command = f"cat {httpx_output_file} | hakrawler -timeout 5 -d 3 | anew -q {temp_output_file}"
    assert run_command(command) == 0, "hakrawler command failed"
    count = int(subprocess.check_output(['wc', '-l', temp_output_file]).split()[0])
    print(colored(f"Found {count} URLs after hakrawler", "green", attrs=["bold"]))
    time.sleep(5)

    print(colored("Running github-endpoints on ", "blue") + colored(domain, "red", attrs=["bold"]))
    command = f"github-endpoints -d {domain} -raw -t YOUR_GITHUB_TOKEN_HERE  -o github-endpoints_temp; cat github-endpoints_temp |  anew -q {temp_output_file}; rm -rf github-endpoints_temp"
    assert run_command(command) == 0, "github-endpoints command failed"
    count = int(subprocess.check_output(['wc', '-l', temp_output_file]).split()[0])
    print(colored(f"Found {count} URLs after github-endpoints", "green", attrs=["bold"]))
    time.sleep(5)

    print(colored("Running cariddi on ", "blue") + colored(domain, "red", attrs=["bold"]))
    command = f"echo {domain} | cariddi -plain | grep {domain} | anew -q {temp_output_file}"
    assert run_command(command) == 0, "cariddi command failed"
    count = int(subprocess.check_output(['wc', '-l', temp_output_file]).split()[0])
    print(colored(f"Found {count} URLs after cariddi", "green", attrs=["bold"]))
    time.sleep(5)

    print(colored("Running gospider on ", "blue") + colored(domain, "red", attrs=["bold"]))
    command = f"gospider -S {httpx_output_file} -t 100 -d 8 -c 10 | grep -o -E '(([a-zA-Z][a-zA-Z0-9+-.]*\\:\\/\\/)|mailto|data\\:)([a-zA-Z0-9\\.\\&\\/\\?\\:@\\+-\\_=#%;,])*' | anew -q {temp_output_file}"
    assert run_command(command) == 0, "gospider command failed"
    count = int(subprocess.check_output(['wc', '-l', temp_output_file]).split()[0])
    print(colored(f"Found {count} URLs after gospider", "green", attrs=["bold"]))
    time.sleep(5)

    print(colored("Running katana on ", "blue") + colored(domain, "red", attrs=["bold"]))
    command = f"katana -list {httpx_output_file} -silent -headless -d 6 -c 20 -jc -f qurl | anew -q {temp_output_file}"
    assert run_command(command) == 0, "katana command failed"
    count = int(subprocess.check_output(['wc', '-l', temp_output_file]).split()[0])
    print(colored(f"Found {count} URLs after katana", "green", attrs=["bold"]))
    time.sleep(5)

    print(colored("Running gourlex on ", "blue") + colored(domain, "red", attrs=["bold"]))
    command = f"gourlex -t {domain} | grep -oE 'https?://[^ ]+' | anew -q {temp_output_file}"
    assert run_command(command) == 0, "gourlex command failed"
    count = int(subprocess.check_output(['wc', '-l', temp_output_file]).split()[0])
    print(colored(f"Found {count} URLs after gourlex", "green", attrs=["bold"]))
    time.sleep(5)

    print(colored("Running orwa on ", "blue") + colored(domain, "red", attrs=["bold"]))
    command = f"echo {domain} | anew -q {domain}_tempfile && bash ~/tools/orwa.sh {domain}_tempfile | egrep 'http|https' | anew -q {temp_output_file} && rm -rf {domain}_tempfile"
    assert run_command(command) == 0, "orwa command failed"
    count = int(subprocess.check_output(['wc', '-l', temp_output_file]).split()[0])
    print(colored(f"Found {count} URLs after orwa", "green", attrs=["bold"]))
    time.sleep(5)

    print(colored("Running urlfinder on ", "blue") + colored(domain, "red", attrs=["bold"]))
    command = f"urlfinder -all -silent -d {domain} | anew -q {temp_output_file}"
    assert run_command(command) == 0, "urlfinder command failed"
    count = int(subprocess.check_output(['wc', '-l', temp_output_file]).split()[0])
    print(colored(f"Found {count} URLs after urlfinder", "green", attrs=["bold"]))
    time.sleep(5)

    print(colored(f"Filtering and deduplicating URLs for {domain}", "green", attrs=['bold']))
    final_command = (
        f"cat {temp_output_file} | egrep 'http|https' | grep {domain} | sort -u | anew -q {output_file} && rm -rf {temp_output_file} && rm -rf {httpx_output_file}"
    )
    run_command(final_command)
    print(colored("Results saved to ", "magenta") + colored(output_file, "yellow", attrs=["bold"]))
    return output_file

def count_lines_in_file(file_path):
    try:
        with open(file_path, 'r') as f:
            return sum(1 for _ in f)
    except Exception as e:
        print(colored(f"Error counting lines in {file_path}: {e}", "red"))
        return 0

def update_index(domain, output_file, index_file):
    line_count = count_lines_in_file(output_file)
    record = f"{domain} - {line_count}\n"
    try:
        with open(index_file, 'a') as f:
            f.write(record)
    except Exception as e:
        print(colored(f"Error updating index file {index_file}: {e}", "red"))

def main():
    print_art()
    parser = argparse.ArgumentParser(description="Passive Crawler Full Stack")
    parser.add_argument('-d', '--domain', help="Single domain to process")
    parser.add_argument('-f', '--file', help="File with list of domains to process")
    parser.add_argument('-o', '--output', required=True, help="Output folder to save the results")
    args = parser.parse_args()

    if not args.domain and not args.file:
        parser.error(colored("At least one of --domain or --file must be specified", "red"))

    domains = []
    if args.domain:
        domains.append(args.domain)
    if args.file:
        try:
            with open(args.file, 'r') as file:
                domains.extend(line.strip() for line in file if line.strip())
        except Exception as e:
            print(colored(f"Error reading file {args.file}: {e}", "red"))
            return

    index_file = os.path.join(args.output, "index.txt")

    for domain in domains:
        output_file = collect_urls(domain, args.output)
        update_index(domain, output_file, index_file)

    print(colored(f"All results saved in {args.output}", "green", attrs=['bold']))
    print(colored(f"Index updated and saved to {index_file}", "green", attrs=['bold']))

if __name__ == "__main__":
    main()
