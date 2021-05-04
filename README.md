# YPS

## License notice

_EXCLUSIVE COPYRIGHT IS OWNED BY STANISLAV AKIMOV (THE AUTHOR).  
THE AUTHOR IS PROVIDING PERMISSION FOR CHECKING (IN ANY POSSIBLE MANNER) MATERIALS IN THIS REPOSITORY TO YALANTIS PYTHON
SCHOOL CURATORS AS A FIRST PART OF REQUIRED TEST TASK DURING SELECTING CANDIDATES TO THE SCHOOL.  
NO OTHER LICENSE IS OFFERING._
___

## What is it?

Part 1 of the [test task](https://docs.google.com/document/d/1QEZeDxCKnXcJu0EKPm9CuHQgN_hkZCOI2iJl1mq3Y50) for Yalantis
Python School.
___

## How to start the application?

To be able to run the application you need to do the following steps (UNIX version):

1. Clone the repository and move to the created folder:

```shell 
$ git clone https://github.com/akimovstv/YPS.git
$ cd YPS
```

2. Create Python virtual environment and activate it.  
   (You need Python version 3.6 or greater)

```shell
$ python3 -m venv .venv
$ source .venv/bin/activate
```

3. Install requirements:

```shell
$ pip install -r requirements.txt
```

4. Run flask:

``` shell
$ env FLASK_APP=app.py FLASK_ENV=development flask run
```

(You might need to add this additional `--port <number_different_from_5000>` option to the last command, if you have
error `Address already in use`)

That is it. The application should be running on http://127.0.0.1:5000/ (or similar).

___
