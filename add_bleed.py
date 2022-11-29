from pathlib import Path
import fitz
import click

MM_TO_PT = 2.8346456692913385


def set_bleed(path: Path, bleed: float):
    bleed = bleed * MM_TO_PT
    doc = fitz.open(path)
    for page in doc:
        bleedbox = fitz.Rect(0, 0, page.cropbox.width, page.cropbox.height)
        trimbox = fitz.Rect(
            bleed,
            bleed,
            page.cropbox.width - (bleed * 2),
            page.cropbox.height - (bleed * 2),
        )
        page.set_bleedbox(bleedbox)
        page.set_trimbox(trimbox)
    save_path = path.parent / (path.stem + "_print" + path.suffix)
    doc.save(save_path)
    doc.close()


@click.command()
@click.option("--path", default="./export/flat", help="Path to files")
@click.option("--bleed", default=2.0, help="Bleed in mm")
def main(path, bleed):
    for file in Path(path).glob("*.pdf"):
        set_bleed(file, bleed)


if __name__ == "__main__":
    main()
