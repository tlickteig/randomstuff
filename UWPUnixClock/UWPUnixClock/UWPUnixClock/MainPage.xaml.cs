using System;
using System.Collections.Generic;
using System.Diagnostics;
using System.IO;
using System.Linq;
using System.Runtime.InteropServices.WindowsRuntime;
using System.Timers;
using Windows.Foundation;
using Windows.Foundation.Collections;
using Windows.UI.Core;
using Windows.UI.Xaml;
using Windows.UI.Xaml.Controls;
using Windows.UI.Xaml.Controls.Primitives;
using Windows.UI.Xaml.Data;
using Windows.UI.Xaml.Input;
using Windows.UI.Xaml.Media;
using Windows.UI.Xaml.Navigation;
using CoreApplication = Windows.ApplicationModel.Core.CoreApplication;

// The Blank Page item template is documented at https://go.microsoft.com/fwlink/?LinkId=402352&clcid=0x409

namespace UWPUnixClock
{
    /// <summary>
    /// An empty page that can be used on its own or navigated to within a Frame.
    /// </summary>
    public sealed partial class MainPage : Page
    {
        private Timer _timer;

        public MainPage()
        {
            this.InitializeComponent();
            _timer = new Timer();
            _timer.Elapsed += new ElapsedEventHandler(TimerElapsed);
            _timer.Interval = 200;
            _timer.Start();
        }

        private async void TimerElapsed(object sender, EventArgs e)
        {
            await CoreApplication.MainView.CoreWindow.Dispatcher.RunAsync(CoreDispatcherPriority.Normal, () =>
            {
                txtEpoch.Text = DateTimeOffset.Now.ToUnixTimeSeconds().ToString();
            });
        }
    }
}
