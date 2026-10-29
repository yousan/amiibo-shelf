package org.l4tp.amiibo;

import android.app.Activity;
import android.content.Intent;
import android.net.Uri;
import android.nfc.NfcAdapter;
import android.nfc.Tag;
import android.nfc.tech.MifareUltralight;
import android.nfc.tech.NfcA;
import android.os.Bundle;
import android.os.VibrationEffect;
import android.os.Vibrator;
import android.webkit.CookieManager;
import android.webkit.JavascriptInterface;
import android.webkit.ValueCallback;
import android.webkit.WebChromeClient;
import android.webkit.WebResourceRequest;
import android.webkit.WebSettings;
import android.webkit.WebView;
import android.webkit.WebViewClient;
import android.widget.Toast;

/**
 * amiibo棚 を WebView で表示し、NFC だけアプリ側で読む。
 * amiibo (NTAG215) の 21〜22 ページには amiibo ID (head 4バイト + tail 4バイト) が暗号化されずに入っているので、
 * かざしただけでどの amiibo か分かる。読んだ結果は window.onNativeTag(uid, amiiboId) で Web 側に渡す。
 */
public class MainActivity extends Activity {
    static final String START_URL = "https://amiibo.l4tp.org/";
    static final String[] OWN_HOSTS = {"l4tp.org", "amiibo.l4tp.org"};
    static final int FILE_REQ = 1;

    WebView web;
    NfcAdapter nfc;
    ValueCallback<Uri[]> fileCb;

    @Override
    protected void onCreate(Bundle saved) {
        super.onCreate(saved);
        web = new WebView(this);
        setContentView(web);

        WebSettings s = web.getSettings();
        s.setJavaScriptEnabled(true);
        s.setDomStorageEnabled(true);
        s.setUserAgentString(s.getUserAgentString() + " AmiiboShelfAndroid/1");
        CookieManager.getInstance().setAcceptCookie(true);

        web.addJavascriptInterface(new Bridge(), "AmiiboAndroid");
        web.setWebViewClient(new WebViewClient() {
            @Override
            public boolean shouldOverrideUrlLoading(WebView v, WebResourceRequest req) {
                Uri u = req.getUrl();
                for (String h : OWN_HOSTS) if (h.equals(u.getHost())) return false;
                startActivity(new Intent(Intent.ACTION_VIEW, u)); // 外部リンクはブラウザで開く
                return true;
            }
        });
        web.setWebChromeClient(new WebChromeClient() {
            @Override
            public boolean onShowFileChooser(WebView v, ValueCallback<Uri[]> cb, FileChooserParams p) {
                if (fileCb != null) fileCb.onReceiveValue(null);
                fileCb = cb;
                try {
                    startActivityForResult(p.createIntent(), FILE_REQ);
                } catch (Exception e) {
                    fileCb = null;
                    return false;
                }
                return true;
            }
        });

        if (saved != null) web.restoreState(saved);
        else web.loadUrl(START_URL);

        nfc = NfcAdapter.getDefaultAdapter(this);
    }

    @Override
    protected void onResume() {
        super.onResume();
        if (nfc == null) return;
        if (!nfc.isEnabled()) {
            Toast.makeText(this, "NFCがオフです。設定でオンにしてください", Toast.LENGTH_LONG).show();
            return;
        }
        // 画面を開いている間はいつでも読む。NDEF の確認は amiibo では不要なので飛ばす
        nfc.enableReaderMode(this, this::onTag,
                NfcAdapter.FLAG_READER_NFC_A | NfcAdapter.FLAG_READER_SKIP_NDEF_CHECK | NfcAdapter.FLAG_READER_NO_PLATFORM_SOUNDS,
                null);
    }

    @Override
    protected void onPause() {
        super.onPause();
        if (nfc != null) nfc.disableReaderMode(this);
    }

    void onTag(Tag tag) {
        String uid = serial(tag.getId());
        String amiiboId = "";
        try {
            byte[] p = readPages(tag, 21);
            if (p != null && p.length >= 8) amiiboId = hex(p, 0, 8);
        } catch (Exception ignored) {
            // amiibo 以外のタグや、読み取り中に離した場合。uid だけ渡す
        }
        final String js = "window.onNativeTag&&window.onNativeTag('" + uid + "','" + amiiboId + "')";
        runOnUiThread(() -> {
            vibrate();
            web.evaluateJavascript(js, null);
        });
    }

    /** READ コマンド (0x30) で指定ページから4ページ (16バイト) 読む */
    static byte[] readPages(Tag tag, int page) throws Exception {
        MifareUltralight mu = MifareUltralight.get(tag);
        if (mu != null) {
            try { mu.connect(); return mu.readPages(page); } finally { mu.close(); }
        }
        NfcA a = NfcA.get(tag);
        if (a == null) return null;
        try { a.connect(); return a.transceive(new byte[]{0x30, (byte) page}); } finally { a.close(); }
    }

    /** Web NFC の serialNumber と同じ形 (04:a1:b2:…) にする。今までに紐付けたタグとそのまま照合できる */
    static String serial(byte[] b) {
        StringBuilder sb = new StringBuilder();
        for (int i = 0; i < b.length; i++) sb.append(i == 0 ? "" : ":").append(String.format("%02x", b[i]));
        return sb.toString();
    }

    static String hex(byte[] b, int from, int to) {
        StringBuilder sb = new StringBuilder();
        for (int i = from; i < to; i++) sb.append(String.format("%02x", b[i]));
        return sb.toString();
    }

    void vibrate() {
        Vibrator v = (Vibrator) getSystemService(VIBRATOR_SERVICE);
        if (v == null) return;
        if (android.os.Build.VERSION.SDK_INT >= 26) v.vibrate(VibrationEffect.createOneShot(80, VibrationEffect.DEFAULT_AMPLITUDE));
        else v.vibrate(80);
    }

    @Override
    protected void onActivityResult(int req, int res, Intent data) {
        if (req == FILE_REQ && fileCb != null) {
            fileCb.onReceiveValue(WebChromeClient.FileChooserParams.parseResult(res, data));
            fileCb = null;
            return;
        }
        super.onActivityResult(req, res, data);
    }

    @Override
    protected void onSaveInstanceState(Bundle out) {
        super.onSaveInstanceState(out);
        web.saveState(out);
    }

    @Override
    public void onBackPressed() {
        if (web.canGoBack()) web.goBack();
        else super.onBackPressed();
    }

    /** Web 側から「アプリの中で動いているか」「NFC が使えるか」を見るためのもの */
    class Bridge {
        @JavascriptInterface public boolean hasNfc() { return nfc != null; }
        @JavascriptInterface public boolean nfcEnabled() { return nfc != null && nfc.isEnabled(); }
    }
}
