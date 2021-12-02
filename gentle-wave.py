# A slow, calm rippling rainbow across the keyboard.

# thanks to ZK Archer for providing an example of how to achieve this effect:
#       https://gist.github.com/zkarcher/b27493baf3a026d6b9dce9069eb4ceec

import colorsys

from tools.effect import Effect

FPS = 1
ADVANCE_PER_SECOND = 0.0125
ADVANCE_PER_FRAME = ADVANCE_PER_SECOND / FPS
WAVES_PER_DEVICE_WIDTH = 0.9
GAMMA = 2.28  # A bit neon looking


class GentleWaveEffect(Effect):
    hue = WAVES_PER_DEVICE_WIDTH

    # Rainbow moves across each device
    def paint(self):
        self.hue += ADVANCE_PER_FRAME

        # Hard-circularize hue, so that the clipping doesn't get precision errors as it grows without bound.
        if self.hue >= 100.0:
            self.hue -= 50.0

        # print("hue={}".format(hue))

        for device in self.devices:
            rows, cols = device.fx.advanced.rows, device.fx.advanced.cols

            for col in range(cols):
                col_hue = self.hue - col * (WAVES_PER_DEVICE_WIDTH / device.fx.advanced.cols)

                for row in range(rows):
                    device.fx.advanced.matrix[row, col] = self.rainbow_rgb(col_hue)

            device.fx.advanced.draw()

    @staticmethod
    def gamma_correct(rgb, gamma):
        return map(lambda x: x ** gamma, rgb)

    def rainbow_rgb(self, hue, sat=1.0, val=1.0, gamma=GAMMA):
        rgb = colorsys.hsv_to_rgb(hue, sat, val)
        rgb = self.gamma_correct(rgb, gamma)
        return tuple(map(lambda x: int(255 * x), rgb))


if __name__ == '__main__':
    e = GentleWaveEffect()
    e.play(FPS)



