# Setting up a working environment for [coverage-crawler](https://github.com/mozilla/coverage-crawler)

Following set up will be done on ubuntu-16.04. You can either use existing Vagrantfile to reproduce required development environment or do a manual setup.

## Software installation


### Vagrant and Virtual Box solution

This is an Ubuntu 16.04.5 LTS (GNU/Linux 4.4.0-116-generic x86_64) installation using vagrant and virtual box.

If you want to configure your own Ubuntu VM via this Vagrantfile you should follow these steps:

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

3. Clone Vagrantfile from this directory to create similar Ubuntu 16.04 machine via python, pip and mercurial tools. Please, copy this file to a folder with a project you want to work on.

4. Run `vagrant up` to create and install your Linux VM:

```
vagrant up
```

Run `vagrant ssh` to connect:
```
vagrant ssh
```
5. Shared folder:
If you connected to vagrant via `vagrant ssh`, you can run `cd /vagrant`  to go to folder shared between vm and your computer.



### Manual set up

You will need python>=3.6, pip for python>=3.6 and [Mercurial](https://www.mercurial-scm.org/) source control management tool installed on your machine to run the script.

Example installation on Ubuntu 16.04:

```
sudo add-apt-repository ppa:jonathonf/python-3.6
sudo apt-get update
sudo apt-get install python3.6 
wget https://bootstrap.pypa.io/get-pip.py
sudo python3.6 get-pip.py
pip3.6 --version
rm get-pip.py
alias pip=pip3.6
alias python=python3.6
sudo add-apt-repository -y ppa:mercurial-ppa/releases
sudo apt-get update
sudo apt-get install -y mercurial
```

## Running script

- No matter which of the set up solutions you have choosen, now you should be able to run the script of coverage-crawler. 

- Stay patient: it may take a while for everything to download. You will need a stable internet connection during artifacts and requirements installation.

1. Install requirements:
```
sudo pip install -r requirements.txt
sudo pip install -r test-requirements.txt
```

2. Download artifacts:
- Try:
```
python download_artifacts.py
```

If you are facing `TaskclusterFailure: rootUrl option is required`, just do following:
```
sudo pip uninstall taskcluster
sudo pip install taskcluster==4.0.1
python download_artifacts.py
```
This is a taskcluster issue which was faced in Oct. 2018. 

3. Run the crawler:
```
python run_crawler.py
```
