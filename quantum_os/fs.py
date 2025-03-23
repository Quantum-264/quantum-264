from os import listdir, stat

def get_applications() -> list[dict[str, str, str]]:
    # fetch a list of the applications that are stored in the filesystem
    applications = []

    for file in listdir("apps"):
        # print(file[:-3])
        if file.endswith("app.py") and file not in ("main.py", "secrets.py"):
            # print(f"App: {file}")
            # convert the filename from "something_or_other.py" to "Something Or Other"
            # via weird incantations and a sprinkling of voodoo
            title = " ".join([v[:1].upper() + v[1:] for v in file[:-3].split("_")])

            applications.append(
                {
                    "file": f"apps.{file[:-3]}",
                    "title": title
                }
            )
        else:
            try:
                stat(f"{file}/{file}.py")
                # convert the filename from "something_or_other.py" to "Something Or Other"
                # via weird incantations and a sprinkling of voodoo
                title = " ".join([v[:1].upper() + v[1:] for v in file.split("_")])

                applications.append(
                    {
                        "file": f"{file}.{file}",
                        "title": title
                    }
                )
            except OSError:
                pass

    # sort the application list alphabetically by title and return the list
    return sorted(applications, key=lambda x: x["title"])

