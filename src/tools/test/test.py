# vim: set expandtab shiftwidth=4 softtabstop=4:
commands = [
    'log warn false error false',
    'open 1a0m',
    '~display /b',
    'style stick',
    'ribbon /b',
    'surface enclose #1 resolution 5',
    'surface close',
    'surface #1',
    'sasa /a',
    'buriedarea /a with /b',
    'color #1 bychain',
    'color @CA purple',
    'light soft',
    'camera field 30',
    'camera',
    'close #1',
    'open pdb:4hhb',
    'color /a@CB tan',
    'colordef wow green',
    'color /c wow',
    '~colordef wow',
    'contacts #1',
    'crossfade 10',
    'delete /c',
    '~display',
    'display /d',
    'display',
    'echo Here we are',
    'color #1 sequential chains cmap rainbow',
    'color /a dodger blue target a',
    'open emdb:1080',
    'fitmap #1 in #2 resolution 10 metric correlation',
    'help fitmap',
    'ks ha',
    'ks rb',
    'title create x text "Look at this" size 36 xpos .2 ypos .8 color yellow',
    'title change x text "Great Scots"',
    'title delete x',
    'lighting',
    'lighting color red',
    'lighting full',
    'list',
    'log hide',
    'log show error false',
    'material specular 1.2 exponent 100',
    'material shiny',
    'molmap #1 5 grid 1',
    'move y 1 20',
    'movie record super 3',
    'wait',
    'movie encode ~/Desktop/test_movie.mp4 quality high',
    'oculus on',
    'oculus off',
    'perframe "turn y 15" frames 10',
    'pwd',
    'roll z',
    'stop',
    'ribbon /b/c',
    '~disp /b/c',
    '~ribbon',
    'run "echo run run run"',
    'sasa /d',
#    'save ~/Desktop/test_image.jpg',  # JPEG support missing, bug #186
    'save ~/Desktop/test_image.png',
    'surface #1',
    'scolor #1 byatom',
    'scolor #1 esp #2',
    'set bg gray silhouettes true',
    'snav on fly true',
    'snav off',
    'split #1',
    'style ball',
    'surface :46-80',
    'surf #1 hide',
    'surf #1 show',
    'close',
    'open 2bbv',
    'sym #1',
    'sym #1 as 4',
    'sym #1 clear',
    'toolshed list',
    'toolshed refresh',
    'toolshed hide cmd_line',
    'toolshed show cmd_line',
    'molmap #1 5 grid 1',
    'volume #2 level .05',
    'volume #2 color tan enclose 1e5',
    'vop gaussian #2 sdev 2',
    'vop subtract #2,3',
    'view',
]
def run_commands(session, commands = commands):
    log = session.logger
    from chimera.core.commands import run
    for c in commands:
        log.info('> ' + c)
        run(session, c)
