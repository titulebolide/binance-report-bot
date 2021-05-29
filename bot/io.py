import requests
import conf
import os
import matplotlib.pyplot as plt
if conf.RICH_PRINTING:
    import rich.console, rich.markdown

def output(msg, img, output, port):
    if output == "print":
        if conf.RICH_PRINTING:
            rich.console.Console().print(
                rich.markdown.Markdown(msg)
            )
        else:
            print(msg)
        if img is not None:
            plt.close()
            fig = plt.figure()
            ax = plt.Axes(fig, [0., 0., 1., 1.])
            ax.set_axis_off()
            fig.add_axes(ax)
            plt.imshow(plt.imread(img))
            plt.show()

    elif output == "http":
        try:
            requests.post("http://127.0.0.1:"+str(port), data={"txt":msg})
            if img is not None:
                requests.post("http://127.0.0.1:"+str(port), data={
                    "img": os.path.join(os.getcwd(), img)
                })
        except requests.exceptions.ConnectionError:
            print(msg)
