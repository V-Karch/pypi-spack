import re


class RequirementParser:
    """
    Parses a Python requirements.txt file and converts
    package requirements into Spack package dependency
    declarations including version constraints and conflicts.
    """

    def __init__(self, filename: str):
        """
        Initialize the parser with the path to a requirements.txt file.

        Args:
            filename (str): Path to the requirements.txt file to parse.
        """
        self.filename = filename

    def parse_specifier(
        self, spec: tuple[str, str]
    ) -> tuple[str | None, str | None, str | None, str | None]:
        """
        Parse a single version specifier tuple (operator, version)
        and classify it into min, max, exact versions or conflicts.

        Args:
            spec (tuple): A tuple of (operator: str, version: str), e.g. ('>=', '2.0')

        Returns:
            tuple: (min_version, max_version, exact_version, conflict_version)
                Each is either a version string or None.
                Only one of exact_version or conflict_version is set if applicable.
        """
        op, ver = spec
        if op == "==":
            return ver, ver, ver, None
        elif op == ">=":
            return ver, None, None, None
        elif op == "<=":
            return None, ver, None, None
        elif op == "<":
            return None, ver, None, None
        elif op == ">":
            return ver, None, None, None
        elif op == "!=":
            return None, None, None, ver
        elif op == "~=":
            return ver, None, None, None
        else:
            return None, None, None, None

    def merge_versions(self, specs: list[tuple[str, str]]) -> tuple[str, list[str]]:
        """
        Combine multiple version specifiers into a single Spack
        version constraint string and collect conflict versions.

        Args:
            specs (list): List of (operator, version) tuples.

        Returns:
            tuple: (version_str: str, conflicts: list)
                version_str is a combined version specifier suitable for Spack,
                conflicts is a list of versions for which conflicts should be declared.
        """
        min_ver = None
        max_ver = None
        exact_ver = None
        conflicts = []

        for spec in specs:
            min_v, max_v, exact_v, conflict_v = self.parse_specifier(spec)
            if conflict_v:
                conflicts.append(conflict_v)
            if exact_v:
                exact_ver = exact_v
            if min_v:
                if (not min_ver) or self.version_greater(min_v, min_ver):
                    min_ver = min_v
            if max_v:
                if (not max_ver) or self.version_less(max_v, max_ver):
                    max_ver = max_v

        if exact_ver:
            version_str = f"@{exact_ver}"
        elif min_ver and max_ver:
            version_str = f"@{min_ver}:{max_ver}"
        elif min_ver:
            version_str = f"@{min_ver}:"
        elif max_ver:
            version_str = f"@:{max_ver}"
        else:
            version_str = ""

        return version_str, conflicts

    def version_greater(self, v1, v2):
        """
        Compare two version strings v1 and v2 to determine if v1 > v2.

        Args:
            v1 (str): Version string like "2.3.1"
            v2 (str): Version string like "2.1"

        Returns:
            bool: True if v1 > v2, else False
        """
        return tuple(map(int, v1.split("."))) > tuple(map(int, v2.split(".")))

    def version_less(self, v1, v2):
        """
        Compare two version strings v1 and v2 to determine if v1 < v2.

        Args:
            v1 (str): Version string like "2.3.1"
            v2 (str): Version string like "2.5"

        Returns:
            bool: True if v1 < v2, else False
        """

        return tuple(map(int, v1.split("."))) < tuple(map(int, v2.split(".")))

    def parse_python_version_marker(self, marker: str):
        """
        Parse a python_version environment marker from requirements.txt
        and convert it to a Spack 'when' version constraint.

        Args:
            marker (str): Marker string like 'python_version >= "3"'.

        Returns:
            str or None: Spack version constraint string like 'python@3:'
                         or None if unsupported or invalid marker.
        """

        marker = marker.strip()
        m = re.match(r'python_version\s*([<>=!]+)\s*[\'"]?([\d\.]+)[\'"]?', marker)
        if not m:
            return None
        op, ver = m.groups()
        major = ver.split(".")[0]

        if op == ">=":
            return f"python@{major}:"
        elif op == "<=":
            return f"python@:{major}"
        elif op == ">":
            try:
                major_int = int(major) + 1
            except:
                major_int = major
            return f"python@{major_int}:"
        elif op == "<":
            try:
                major_int = int(major) - 1
            except:
                major_int = major
            return f"python@:{major_int}"
        elif op == "==":
            return f"python@{major}"
        elif op == "!=":
            return None
        else:
            return None

    def parse(self) -> list[str]:
        """
        Parse the requirements.txt file and convert each requirement line
        into Spack dependency or conflict declarations.

        Returns:
            list[str]: List of strings containing Spack
                       depends_on(...) and conflicts(...) declarations.
        """
        results = []
        conflicts = []

        with open(self.filename, "r") as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith("#"):
                    continue

                parts = line.split(";", 1)
                req_part = parts[0].strip()
                env_marker = parts[1].strip() if len(parts) > 1 else None

                req_part = re.split(r"\[", req_part)[0].strip()

                match = re.match(r"^([a-zA-Z0-9_\-]+)(.*)$", req_part)
                if not match:
                    continue
                pkg, rest = match.groups()
                spec_parts = re.findall(r"([><=!~]+)\s*([\d\.]+)", rest)

                spack_pkg = f"py-{pkg.lower().replace('_', '-')}"
                version, conflict_versions = self.merge_versions(spec_parts)

                when_clause = ""
                if env_marker and env_marker.startswith("python_version"):
                    when_val = self.parse_python_version_marker(env_marker)
                    if when_val:
                        when_clause = f', when="{when_val}"'

                # Add depends_on line
                results.append(
                    f'depends_on("{spack_pkg}{version}"{when_clause}, type=("build", "run"))'
                )

                # Add conflicts lines for each conflict version
                for cv in conflict_versions:
                    conflicts.append(f'conflicts("{spack_pkg}@{cv}")')

        return results + conflicts
