# KHIDL

***NOTE: THIS PROJECT IS NOT AFFILIATED WITH KHINSIDER.***

Download soundtracks from [KHInsider](https://downloads.khinsider.com)
with a simple CLI.

## Installing

Download the latest version from PyPi using pip with the following command.

```sh
pip install khinsider-dl
```

You can also download the .whl file from the github releases [here](https://github.com/qwerinope/khidl/releases)
and install it with `pip install`.

There's an AUR package available too: [`python-khidl`](https://aur.archlinux.org/packages/python-khidl)

## Usage

### Download

```sh
khidl download [soundtrack id/url]
```

This command will download the specified soundtrack to a named directory
in the current working directory.

```sh
khidl download minecraft output --format flac --no-images
```

This command will download the minecraft soundtrack to a directory called output.
If the second positional command is left empty it will download the soundtrack
to a new directory named after the requested soundtrack.

The `--format` flag can be used to specify the requested music format.
All soundtracks are available in mp3 format.
Most soundtracks have other optional formats, like flac or m4a.
If a soundtrack is unavailable in the requested format,
the program will stop and notify the user about available formats.
If the user specifies the format as `nomusic`, the program will not download music, only images.

The `--no-images` argument makes sure `khidl` doesn't download images
belonging to the soundtrack.


For more detail please read the help page:

```sh
khidl download -h
```

### Search

```sh
khidl search [query]
```

This command will query the KHInsider database for soundtracks containing the query.
Afterwards it will print the result to the terminal in a pretty table.

```sh
khidl search lonely rolling star --song
```

This command will search the database for songs with the query 'lonely rolling star'.
Afterwards it will return all soundtracks with a song that features the query.

`khidl search` returns the name and ID of the soundtrack,
as well as the year of release.
You need to pass the ID into the [download function](#download)
to download the ost.

Note that searcing for a specific song is considerably slower,
it can take about 10 seconds to show data.

### Batch

To create the default configuration, run

```sh
khidl batch --init
```

This creats a `soundtrack.json`. In this file,
you can specify multiple soundtracks to be downloaded.
For each soundtrack you can set the requested download format.

The example showcases all options and ways to configure it.
There is a JSON schema included, please use it,
as it will warn you before running the script if you have made an error.

The script will validate the json before parsing it.
This behavior can be stopped by using `-f`/`--force`.
This is intended for testing and development only.
If the formatting is wrong the program will crash.

#### Special thanks

Special thanks to KHInsider for the incredible database.  
Special thanks to [obskyr's khinsider.py](https://github.com/obskyr/khinsider) project.
