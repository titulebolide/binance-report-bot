import requests
import conf
import os
import matplotlib.pyplot as plt
import logging
import brb

if conf.APPRISE_URL != "":
    import apprise
if conf.RICH_PRINTING:
    import rich.console, rich.markdown


def output(msg, img, quiet):
    if not quiet:
        if conf.RICH_PRINTING:
            rich.console.Console().print(rich.markdown.Markdown(msg))
        else:
            print(msg)
        if img is not None:
            plt.close()
            fig = plt.figure()
            ax = plt.Axes(fig, [0.0, 0.0, 1.0, 1.0])
            ax.set_axis_off()
            fig.add_axes(ax)
            plt.imshow(plt.imread(img))
            plt.show()

    if brb.notifier is not None:
        brb.notifier.notify(
            body=msg, body_format=apprise.NotifyFormat.MARKDOWN, attach=img
        )
