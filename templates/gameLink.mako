<%page args="time, base"/><%! from tntfl.game import Game %><a href="${base}game/${time}/">${Game.formatTime(time)}</a>
