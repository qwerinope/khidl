# KHIDL

Download soundtracks from [KHInsider](https://downloads.khinsider.com)
with a simple CLI.

## Installing

Download the latest `.whl` file from [here](https://github.com/qweri0p/khidl/releases).
Then run:

```sh
pip install khidl.whl
```

## Basic Usage

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
It is constrained to mp3, flac and m4a.
If a soundtrack is unavailable in the requested format,
the program will stop and notify the user.

the `--no-images` argument makes sure `khidl` doesn't download images
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
For each soundtrack you can set the requested download format
(either mp3, flac or m4a).

The example showcases all options and ways to configure it.
There is a JSON schema included, please use it,
as it will warn you before running the script if you have made an error.
