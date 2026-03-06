#!/usr/bin/env python3
"""
Script name: bundlegen.py

Purpose of script: Creates Starbundle ZIP files for the purpose of adding files to IntelliSTAR 2-based devices.

Author: physicsprop

Date Created: 03-22-2023

Notes: Can only create "<Add..>" changes. "<Delete..." actions are too destructive to automate.
"""

import os
import shutil
import uuid
from pathlib import Path
from datetime import datetime
from zipfile import ZipFile, ZIP_DEFLATED


class BundleGenerator:
    def __init__(self):
        self.arrlst = []
        self.bundletype = ""
        self.bundletarget = ""
        self.bundleheadend = ""
        self.headend = ""
        self.version = ""
        self.type = ""
        self.target = ""
        self.date = ""

    def get_target_bundle_information(self):
        """Collect all files from input directory and gather user input for bundle configuration."""
        # Get all files from input directory recursively
        input_path = Path("./input")
        if not input_path.exists():
            print("ERROR: './input' directory does not exist.")
            return False

        self.arrlst = [str(f) for f in input_path.rglob("*") if f.is_file()]

        # Begin user interaction
        print("Please specify the type of bundle to create.")
        print("1. Changeset (viz assets)\n2. Managed (i2 products/flavors)")
        self.bundletype = input().strip()

        if not self.bundletype:
            print("No option was selected. Exiting...")
            return False

        print("Please specify bundle target.")
        print(
            "1. Any Domestic_Universe (I2HD/I2XD)\n2. Any Domestic_SD_Universe (I2JR)\n3. Specific Headend ID\n4. Any STAR type"
        )
        self.bundletarget = input().strip()

        if not self.bundletarget:
            print("There was no response, assuming option 4.\n")
            self.bundletarget = "4"

        if self.bundletarget == "3":
            print("Please specify Headend ID to apply changes to.")
            self.bundleheadend = input().strip()
            self.headend = f"heId='{self.bundleheadend}'"

        print(
            "Please specify version string. This will be used by the I2 to determine if files need to be replaced or updated when a bundle is processed."
        )
        self.version = input().strip()

        print("Running checks and setting variables...")

        if self.bundletype == "1":
            self.type = "Changeset"
        elif self.bundletype == "2":
            self.type = "Managed"

        if self.bundletarget == "1":
            self.target = 'starFlags="Domestic_Universe"'
        elif self.bundletarget == "2":
            self.target = 'starFlags="Domestic_SD_Universe"'
        else:
            self.target = ""

        file_count = len(self.arrlst)
        print(f"Going to create a {self.type} bundle containing {file_count} files.")

        if self.bundletarget == "3":
            print(f"This bundle will only apply to I2 Headend ID {self.bundleheadend}")
        elif self.bundletarget == "1":
            print("This bundle will only apply to Domestic_Universe (I2XD/HD) units.")
        elif self.bundletarget == "2":
            print("This bundle will only apply to Domestic_SD_Universe (I2JR) units.")
        elif self.bundletarget == "4":
            print("This bundle will only apply to any unit.")

        print(
            f"The output file will be named StarBundle-{self.type}-{self.version}.zip and will be stored in the output folder."
        )
        print("Ready to commit!")
        print("Press enter to commit bundle.")
        input()

        return True

    def prepare_target_bundle_folder(self):
        """Create the output folder structure for the bundle."""
        try:
            print("Preparing target folder.")
            bundle_path = Path(
                f"./output/StarBundle-{self.type}-{self.version}/MetaData"
            )
            bundle_path.mkdir(parents=True, exist_ok=True)
            return True
        except Exception as e:
            print(f"FATAL: Unable to create output folder. Error: {e}")
            return False

    def start_target_bundle_manifest(self):
        """Write the XML manifest header."""
        self.date = datetime.now().strftime("%m/%d/%Y")
        print("Writing manifest header.")

        manifest_path = Path(
            f"./output/StarBundle-{self.type}-{self.version}/MetaData/manifest.xml"
        )

        with open(manifest_path, "w") as f:
            f.write("<StarBundle>\n")
            f.write(f"<Version>{self.version}</Version>\n")
            f.write(f"<ApplyDate>{self.date}</ApplyDate>\n")
            f.write(f"<Type>{self.type}</Type>\n")
            f.write("<FileActions>\n")

    def commit_files_to_target_bundle(self):
        """Copy files to bundle and add entries to manifest."""
        print("Preparing to commit files to target StarBundle.")
        manifest_path = Path(
            f"./output/StarBundle-{self.type}-{self.version}/MetaData/manifest.xml"
        )

        for file in self.arrlst:
            # Get relative path (remove 'input' prefix)
            relpath = str(Path(file).relative_to("./input"))
            relpath = relpath.replace("\\", "/")  # Normalize path separators

            # Generate GUID for file
            guid = str(uuid.uuid4())

            try:
                print(f"Commiting {relpath} to bundle.")
                dest_file = Path(
                    f"./output/StarBundle-{self.type}-{self.version}/{guid}"
                )
                shutil.copy2(file, dest_file)

                # Build manifest entry
                manifest_entry = (
                    f"<Add src='{guid}' dest='{relpath}' version='{self.version}'"
                )
                if self.target:
                    manifest_entry += f" {self.target}"
                if self.headend:
                    manifest_entry += f" {self.headend}"
                manifest_entry += " />\n"

                # Append to manifest
                with open(manifest_path, "a") as f:
                    f.write(manifest_entry)

            except Exception as e:
                print(
                    f"Unable to commit {relpath} to bundle. This file will be skipped. Error: {e}"
                )

    def finalize_target_bundle(self):
        """Close the manifest and create the ZIP file."""
        print("Committing final manifest.")
        manifest_path = Path(
            f"./output/StarBundle-{self.type}-{self.version}/MetaData/manifest.xml"
        )

        with open(manifest_path, "a") as f:
            f.write("</FileActions>\n")
            f.write("</StarBundle>\n")

        try:
            print("Committing StarBundle to ZIP file.")
            bundle_dir = Path(f"./output/StarBundle-{self.type}-{self.version}")
            zip_path = Path(f"./output/StarBundle-{self.type}-{self.version}.zip")

            with ZipFile(zip_path, "w", ZIP_DEFLATED) as zipf:
                # Walk through the bundle directory
                for root, dirs, files in os.walk(bundle_dir):
                    for file in files:
                        file_path = Path(root) / file
                        # Calculate relative path from bundle dir
                        arcname = file_path.relative_to(bundle_dir)
                        zipf.write(file_path, arcname)

            print(f"Bundle created successfully: {zip_path}")

        except Exception as e:
            print(f"Unable to commit bundle to ZIP file. Error: {e}")

    def run(self):
        """Main execution flow."""
        print("BundleGen.py - StarBundle generator for i2s, in Python!")
        print("A reimplementation of starbundle-utils by Project Aries")

        if not self.get_target_bundle_information():
            return

        if not self.prepare_target_bundle_folder():
            return

        self.start_target_bundle_manifest()
        self.commit_files_to_target_bundle()
        self.finalize_target_bundle()


if __name__ == "__main__":
    generator = BundleGenerator()
    generator.run()
