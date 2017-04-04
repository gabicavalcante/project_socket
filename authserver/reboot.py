def reboot(port):
    """
    Method to reboot port
    source: http://stackoverflow.com/questions/7703797/need-to-close-python-socket-find-the-current-running-server-on-my-dev-environm
    :param port:
    :return:
    """
    import re
    import commands
    s = commands.getoutput('lsof -i :{0}'.format(port))
    try:
        p_id = re.findall('.*?Python\s+[0-9]{4,7}', s)[0].split(' ')[-1]
    except IndexError:
        p_id = None
    p_id = int(p_id) if p_id else None
    if p_id:
        commands.getoutput('kill -9 {}'.format(p_id))