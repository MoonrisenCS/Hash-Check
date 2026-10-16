import argparse
import hashlib
from pathlib import Path
import json
import random
import sys

def file_exists(path: Path) -> bool:
    if path.is_file(): # Checks if the file exists
        return True
    else:
        return False
    # END IF
# END FUNCTION

def write_hash(file: Path, text: str):
    with file.open("a") as f:
        f.write(f"{text}\n")
    # CLOSE FILE

def generate_hash(path: Path, hash: str) -> str:
    global hash_list

    if file_exists(path):

        if hash == "sha256":
            hasher = hashlib.sha256() # Creates a SHA-256 hash object

            with path.open("rb") as file: # Opens file in read-binary mode
                while chunk := file.read(4096): # Reads up to 4096 bytes; stops at EOF
                    hasher.update(chunk) # Updates the hash with the current chunk

            return hasher.hexdigest() # Returns the SHA-256 digest as hexadecimal text
        
        elif hash == "md5":
            hasher = hashlib.md5() # Creates an MD5 hash object
            
            with path.open("rb") as file: # Opens file in read-binary mode
                while chunk := file.read(4096): # Reads up to 4096 bytes; stops at EOF
                    hasher.update(chunk) # Updates the hash with the current chunk

            return hasher.hexdigest() # Returns the MD5 digest as hexadecimal text

        else:
            print("Hash algortihm does not exist and/or is not supported.")
            sys.exit()

        # END IF

    else:
        hash_list = Path("hashList.json")
        hash_list.write_text("")
        return generate_hash(path=hash_list, hash=hash)
    # END IF
# END FUNCTION

def verify_hash(file_path: Path, hash_algorithm: str, hash_list: Path, key: str):
    hash_to_compare: str = generate_hash(file_path, hash_algorithm) # Calculate he hash of the file we wish to verify

    with hash_list.open("r") as hl:
        hashes: list = json.load(hl)

    found: bool = False
    for i in range(len(hashes)):
        if hashes[i]["Unlock Key"] == key and hashes[i]["Algorithm"] == hash_algorithm:
            pos: int = i
            found = True
        # END IF
    # END LOOP
    
    if found == True:
        if hashes[pos]["Hash Value"] == hash_to_compare:
            return True
        else:
            return False
    else:
        print("Verification key or Hash Algorithm invalid")
        sys.exit()




def main(hash_file: Path):
    parser = argparse.ArgumentParser(description="Custom CLI for Generating and Verifying SHA256 file hashes") # Create the top-level parser

    subparsers = parser.add_subparsers(dest="command", required=True, help="Available commands") # Add subcommands manager

    gen_parser = subparsers.add_parser("generate", help="Generate a files SHA256 or MD5 hash value.", ) # Add 'generate' subcommand
    gen_parser.add_argument("file", help="Path to the file you wish to generate a hash for.")
    gen_parser.add_argument("-a", "--algo", choices=["md5", "sha256"], default = "sha256", help="Hashing Algorithms")

    # VERIFY LATER

    ver_parser = subparsers.add_parser("verify", help="Verify a files hash value") # Add 'verify' subcommand
    ver_parser.add_argument("file", help="Path to the file you wish to verify a hash for.")
    ver_parser.add_argument("key", help="The Unlock Key to gain permission to verify")
    ver_parser.add_argument("-a", "--algo", choices=["md5", "sha256"], default = "sha256", help="Hashing Algorithms")

    args = parser.parse_args()

    file: Path = Path(args.file)
    hash_algorithm: str = args.algo

    if args.command == "generate":
        unlock_key = random.randint(1000, 9999) # generate an unlock key
        print(f"Generating {hash_algorithm} hash for file {file}")
        hashed_file_value: str = generate_hash(path=file, hash=hash_algorithm) # Call generate_hash() func and get the hashed value
        print(f"The {hash_algorithm} hashed value of the file is: {hashed_file_value}")
        

        data: dict = {
            "Algorithm": f"{hash_algorithm}",
            "Hash Value": f"{hashed_file_value}",
            "Unlock Key": f"{unlock_key}"
        } # Set the data up for saving to a file

        with hash_file.open("r") as hf:
            try:
                existing_data: list = json.load(hf)
            except json.JSONDecodeError: # Incase of data corruption or other issue
                existing_data: list = []
        # CLOSE FILE

        data_exists: bool = any(record.get("Hash Value") == data["Hash Value"] for record in existing_data) # Check that the file location appears, to prevent a duplicate.
        if not data_exists:
            print(f"The key to unlock this file for hash verifying is: {unlock_key}\nKeep this number safe somewhere.")
            existing_data.append(data)

            with hash_file.open("w") as hf:
                json.dump(existing_data, hf, indent=4) # Write data to json file
            # CLOSE FILE
        # END IF
    elif args.command == "verify":
        key: str = args.key # get unlock key from arguments
        print(f"Verifying {hash_algorithm} hash for file {file}")
        verified = verify_hash(file_path=file, hash_algorithm=hash_algorithm, hash_list=hash_file, key=key)

        if verified:
            print("The file's hash has been verified, there has been no modifications or corruption.")
        else:
            print("The file's hash did not match, there may have been modifications or corruption to the original file.")
    # END IF

hash_list = Path("hashList.json")
main(hash_file=hash_list)