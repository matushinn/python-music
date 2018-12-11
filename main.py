import os
from kivy.app import App
from kivy.core.audio import SoundLoader
from kivy.properties import ObjectProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.popup import Popup


class PopupChooseFile(BoxLayout):
    # 現在のカレントディレクトリ。FileChooserIconViewのpathに渡す
    current_dir = os.path.dirname(os.path.abspath(__file__))

    # MusicPlayerクラス内で参照するための設定
    select = ObjectProperty(None)
    cancel = ObjectProperty(None)


class MusicPlayer(BoxLayout):
    audio_button = ObjectProperty(None)  # >や||のボタンへのアクセス
    status = ObjectProperty(None)  # 画面中央のお知らせとなるテキスト部分
    sound = None

    def choose(self):
        """Choose File押下時に呼び出され、ポップアップでファイル選択させる"""

        content = PopupCho
        seFile(select=self.select, cancel=self.cancel)
        self.popup = Popup(title="Select MP3", content=content)
        self.popup.open()

    def play_or_stop(self):
        """||や>押下時。再生中なら一時停止、停止中なら再生する"""

        # ファイルが選択されていればTrue
        if self.sound:

            # 再生中
            if self.sound.state == "play":
                self.sound_position = self.sound.get_pos()  # 再生位置の保存
                self.sound.stop()
                self.audio_button.text = ">"
                self.status.text = 'Stop {}'.format(self.sound_name)

            # 一時停止中
            elif self.sound.state == "stop":
                self.sound.play()
                self.sound.seek(self.sound_position)  # 再生位置の復元
                self.audio_button.text = "||"
                self.status.text = 'Playing {}'.format(self.sound_name)

        # ファイルを選択してないなら、選択しろと画面中央に表示
        else:
            self.status.text = 'Please Select MP3'

    def cancel(self):
        """ファイル選択画面でキャンセル"""

        self.popup.dismiss()

    def select(self, path):
        """ファイル選択画面で、ファイル選択時"""

        # 既に再生している物があればストップ
        if self.sound:
            self.sound.stop()

        self.sound = SoundLoader.load(path)
        self.sound_name = os.path.basename(path)

        # 再生を試みて、できない（mp3じゃない）ならexcept。MP3にしろとメッセージ
        try:
            self.sound.play()
        except AttributeError:
            self.status.text = 'Should MP3'
        else:
            self.audio_button.text = "||"
            self.status.text = 'Playing {}'.format(self.sound_name)
        finally:
            self.popup.dismiss()


class Music(App):
    icon = "ico.png"

    def build(self):
        return MusicPlayer()


if __name__ == "__main__":
    Music().run()