# Breath of the Wild Actor Tool, edits actor files fin LoZ:BotW
# Copyright (C) 2020 GingerAvalanche (chodness@gmail.com)
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published
# by the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

import oead
from pathlib import Path
from pymsyt import Msbt
from typing import Dict

from . import util


class ActorTexts:
    _texts: Dict[str, str]
    _misc_texts: dict
    _actor_name: str
    _profile: str

    def __init__(self, pack: Path, profile: str):
        self._texts = {}
        self._misc_texts = {}
        self._actor_name = pack.stem
        self._profile = profile
        root_dir = pack.parent
        while True:
            if (root_dir / "Actor").exists() or (
                not root_dir.stem == "Actor" and (root_dir / "Pack").exists()
            ):
                break
            root_dir = root_dir.parent
        settings = util.BatSettings()
        lang = settings.get_setting("lang")
        text_pack = root_dir / f"Pack/Bootup_{lang}.pack"
        if not text_pack.exists():
            root_dir = Path(settings.get_setting("update_dir"))
            text_pack = root_dir / f"Pack/Bootup_{lang}.pack"
        text_sarc = oead.Sarc(text_pack.read_bytes())
        message = f"Message/Msg_{lang}.product.ssarc"
        message_sarc = oead.Sarc(oead.yaz0.decompress(text_sarc.get_file(message).data))
        msbt = message_sarc.get_file(f"ActorType/{self._profile}.msbt")
        if not msbt:
            return
        msyt = Msbt.from_binary(bytes(msbt.data)).to_dict()
        del text_sarc
        del message_sarc
        del msbt
        for e in msyt["entries"]:
            if self._actor_name in e:
                entry = e.replace(f"{self._actor_name}_", "")
                self._texts[entry] = ""
                for control_type in msyt["entries"][e]["contents"]:
                    if "text" in control_type:
                        self._texts[entry] = f"{self._texts[entry]}{control_type['text']}"

    def set_texts(self, texts: Dict[str, str]) -> None:
        self._texts = texts

    def get_texts(self) -> Dict[str, str]:
        return self._texts

    def set_actor_name(self, name: str) -> None:
        self._actor_name = name

    def write(self, root_str: str, be: bool) -> None:
        if self._texts:
            lang = util.BatSettings().get_setting("lang")
            text_pack = Path(f"{root_str}/Pack/Bootup_{lang}.pack")
            text_pack_load = text_pack
            if not text_pack.exists():
                text_pack.parent.mkdir(parents=True, exist_ok=True)
                text_pack.touch()
                text_pack_load = Path(util.find_file(Path(f"Pack/Bootup_{lang}.pack")))
            text_sarc = oead.Sarc(text_pack_load.read_bytes())
            text_sarc_writer = oead.SarcWriter.from_sarc(text_sarc)
            message = f"Message/Msg_{lang}.product.ssarc"
            message_sarc = oead.Sarc(oead.yaz0.decompress(text_sarc.get_file(message).data))
            message_sarc_writer = oead.SarcWriter.from_sarc(message_sarc)
            msbt_name = f"ActorType/{self._profile}.msbt"
            msyt = Msbt.from_binary(bytes(message_sarc_writer.files[msbt_name])).to_dict()
            for key, text in self._texts.items():
                msyt["entries"][f"{self._actor_name}_{key}"] = {"contents": [{"text": text}]}
            message_sarc_writer.files[msbt_name] = Msbt.from_dict(msyt).to_binary(be)
            message_bytes = message_sarc_writer.write()[1]
            text_sarc_writer.files[message] = oead.yaz0.compress(message_bytes)
            text_pack.write_bytes(text_sarc_writer.write()[1])
