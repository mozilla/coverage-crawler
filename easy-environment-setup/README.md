# Setting up a working environment for [coverage-crawler](https://github.com/mozilla/coverage-crawler)

Following set up will be done on ubuntu-16.04. You can either use existing Vagrantfile to reproduce required development environment or do a manual setup.

## Software installation

### Vagrant and Virtual Box solution

This is an Ubuntu 16.04.5 LTS (GNU/Linux 4.4.0-116-generic x86_64) installation using vagrant and virtual box.

If you want to configuare your own Ubuntu VM via this Vagrantfile you should follow these steps:

1. Install VirtualBox.
2. Install Vagrant.

- You can download via website:
Vagrant can be downloaded from HashiCorp [website](https://www.vagrantup.com/).
VirtualBox from [here](https://www.virtualbox.org/).


- or via brew (Mac OS):
```
ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"
brew cask install vagrant
brew cask install virtualbox
```

3. Clone Vagrantfile from this directory to create similar Ubuntu 16.04 machine via python, pip and mercurial tools.

4. Run `vagrant up` to create and install your Linux VM:

```
vagrant up
```

Run `vagrant ssh` to connect:
```
vagrant ssh
```


### Manual set up

You will need python>=3.5, pip for python>=3.5 and [Mercurial](https://www.mercurial-scm.org/) source control management tool installed on your machine to run the script.

Example installation on Ubuntu 16.04:

```
sudo apt-get install python3.5
wget https://bootstrap.pypa.io/get-pip.py
sudo python3.5 get-pip.py
pip3.5 --version
rm get-pip.py
sudo add-apt-repository -y ppa:mercurial-ppa/releases
sudo apt-get update
sudo apt-get install -y mercurial
```

## Running script

- No matter which of the set up solutions you have choosen, now you should be able to run the script of coverage-crawler. 

- Stay patient: it may take a while for everything to download. You will need a stable internet connection during artifacts and requirements installation.

1. Install requirements:
```
sudo pip3 install -r requirements.txt
sudo pip3 install -r test-requirements.txt
```

2. Download artifacts:
- Try:
```
python3 download_artifacts.py
```

If you are facing `TaskclusterFailure: rootUrl option is required`, just do following:
```
sudo pip3  uninstall taskcluster
sudo pip3  install taskcluster==4.0.1
python3 download_artifacts.py
```
This is a taskcluster issue which was faced in Oct. 2018. 

3. Run the crawler:
```
python3 run_crawler.py
```
