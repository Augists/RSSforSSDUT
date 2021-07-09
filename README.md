# RSS for DUT-EDA

Provide RSS link for the undergraduate notice in DUT EDA(大连理工大学开发区校区)

## Preparation

### python3

* macOS

`brew install python3`

* ubuntu

`sudo apt install python3`

### bs4

Python use `requests` and `bs4` to get the content of undergraduate notice on [https://ssdut.dlut.edu.cn](https://ssdut.dlut.edu.cn) and [https://ise.dlut.edu.cn](https://ise.dlut.edu.cn). You may also have to install `requests` if needed

`pip3 install bs4`

### rfeed

[`rfeed`](https://github.com/svpino/rfeed) is a library to generate RSS 2.0 feeds in Python. It's based on the work from Andrew Dalke in the [PyRSS2Gen](http://www.dalkescientific.com/Python/PyRSS2Gen.html) library

[`rfeed`](https://github.com/svpino/rfeed) is extensible, and in my opinion very easy to use. Besides the standard RSS 2.0 specification, it also includes iTunes support for podcast feeds.

This project use `rfeed` to generate `atom.xml` file

```python
git clone https://github.com/svpino/rfeed.git
cd rfeed
python setup.py install
```

### apache2

Frankly speaking, you can choose your favorite Http Server, and as for me, I choose apache2 to provide http web page

Default `atom.xml` path:

* Software: `/var/www/html/atom.xml`
* ISE: `/var/www/html/ise/atom.xml`

```bash
apt install apache2
cd /etc/apache2
vi apache2.conf
```

Start your apache2 server and test

## Usage

1. `git clone https://github.com/Augists/RSSforSSDUT.git`
2. `cd RSSforSSDUT`
3. create your `info.txt` file and just write into the first line with freedom (if needed)
4. choose your directory
	* Software
	* ISE
5. `chmod +x runssdut.sh`
6. `nohup ./runssdut.sh > log.out 2>&1 &`

then the shell script will run in slience, with check for updating in every 50 or 60 seconds

You can `ps -ef` to list the jobs behind and find that

```bash
./runssdut.sh
python3 ssdut.py
```

or

```bash
./runssdut.sh
sleep 50s
```

Just `kill -9 job_id` to stop your RSS job

## MIT License

```LICENSE
Copyright (c) 2021 Augists ZDCZ

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```
