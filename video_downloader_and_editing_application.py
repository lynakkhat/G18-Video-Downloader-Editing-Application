import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from tkinter import messagebox
import tkinter as tk
from PIL import Image, ImageTk
import yt_dlp as ytdl
from yt_dlp import YoutubeDL 
from tkinter import filedialog
import os
import threading
import ttkbootstrap as ttkb  
import cv2
from pydub import AudioSegment
from moviepy.video.io.VideoFileClip import VideoFileClip
import yt_dlp

# Global variables to hold references to windows
download_video_window = None
youtube_download_window = None
facebook_download_window = None
website_window = None
audio_download_window = None  
playlist_download_window = None
extract_image_window = None
cut_window = None
cut_audio_window = None
cut_video_window = None
selected_file = None 

# Function to handle the Download Video window
def download_video():
    global download_video_window
    root.withdraw()  
    download_video_window = ttk.Toplevel(root)
    download_video_window.title("Download Video")
    download_video_window.geometry("600x400")  
    download_video_window.configure(bg="#333333")
    download_video_window.attributes('-fullscreen', True)  

    ttk.Label(download_video_window, text="", background="#333333").pack(pady=130)

    ttk.Label(download_video_window, text="Select Video Source", font=("Helvetica", 38, "bold"), foreground="white", background="#333333").pack()

    ttk.Label(download_video_window, text="", background="#333333").pack(pady=15)

    style = ttkb.Style()
    style.configure("info.TButton",font=("Helvetica", 16, "bold"), padding=(0, 10))  

    ttk.Button(download_video_window, text="YouTube", bootstyle=INFO, command= lambda: show_youtube_download(), width=40, style="info.TButton").pack(pady=15)
    ttk.Button(download_video_window, text="Facebook", bootstyle=INFO, command=lambda: show_facebook_download(), width=40, style="info.TButton").pack(pady=15)
    ttk.Button(download_video_window, text="Website", bootstyle=INFO, command=lambda:  show_website_download(), width=40, style="info.TButton").pack(pady=15)
    ttk.Button(download_video_window, text="Back", bootstyle=DANGER, command=lambda: [download_video_window.destroy(), root.deiconify()], width=20, style="danger.TButton").pack(pady=30)

#--------------------------------------------------------------------------------------------------------------------------------------------------------
# Function to show YouTube download interface
def show_youtube_download():
    global youtube_download_window, download_video_window

    if download_video_window:
       download_video_window.destroy()

    youtube_download_window = ttk.Toplevel(root)
    youtube_download_window.title("Download Video from YouTube")
    youtube_download_window.geometry("800x500")
    youtube_download_window.configure(bg="#333333")
    youtube_download_window.attributes('-fullscreen', True)  

    header_frame = tk.Frame(youtube_download_window, bg="#333333", height=100)
    header_frame.pack(fill=X)

    header_label = tk.Label(header_frame, text="YouTube Downloader Tool", font=("Arial", 38, "bold"),bg="#333333",fg="white",)
    header_label.pack(pady=30)

    main_frame = tk.Frame(youtube_download_window, bg="#555555", bd=2, relief="ridge", highlightbackground="#444444", highlightthickness=2, pady=20)
    main_frame.place(relx=0.5, rely=0.5, anchor="center", width=1000, height=600)

    title_label = tk.Label(main_frame, text="YouTube Video Downloader", font=("Helvetica", 30, "bold"), fg="white", bg="#555555")
    title_label.pack(pady=30)

    url_label = tk.Label(main_frame, text="Please enter a valid YouTube URL below:", width=40, font=("Helvetica", 16), fg="white", bg="#555555")
    url_label.pack(pady=10)

    url_entry = tk.Entry(main_frame, font=("Helvetica", 14), width=40)
    url_entry.pack(pady=15)


    style = ttkb.Style()
    style.configure("danger.TButton", font=("Helvetica", 14, "bold"), padding=(0, 10))  

    tk.Button(main_frame, text="Download Video", width=15, height=2, bg="#0078D7", fg="white", font=("Helvetica", 14),command=lambda: start_download(url_entry.get())).pack(pady=50)

    global progress_label
    progress_label = ttk.Label(main_frame, text="", font=("Helvetica", 14),foreground="white")
    progress_label.pack(pady=0)

    ttk.Button(youtube_download_window, text="Back", bootstyle=DANGER, command=lambda: [youtube_download_window.destroy(), open_video_window()], width=10).place(relx=0.0, rely=1.0, anchor="sw", x=690, y=-290)  
    ttk.Button(youtube_download_window, text="Exit", bootstyle=DANGER, command=root.quit, width=10).place(relx=1.0, rely=1.0, anchor="se", x=-690, y=-290)  


# Function to handle the download process
def start_download(url):
    def select_folder():
        folder = filedialog.askdirectory(title="Select Folder to Save Video")
        if not folder:
            messagebox.showwarning("Warning", "No folder selected!")
        return folder

    def download_progress(d):
        if d['status'] == 'downloading':
            percent = d['_percent_str']
            eta = d.get('eta', 'N/A')  
            progress_label.config(text=f"Downloading: {percent} | ETA: {eta}s", foreground="blue")
            youtube_download_window.update_idletasks()

    if not url:
        messagebox.showerror("Error", "Please enter a valid video URL")
        return

    folder = select_folder()
    if not folder:
        return

    ydl_opts = {
        'format': 'best',
        'outtmpl': os.path.join(folder, '%(title)s.%(ext)s'),
        'progress_hooks': [download_progress],
    }

    # Function to run the download process in a separate thread
    def download_task():
        try:
            progress_label.config(text="Preparing download...", foreground="#e62117")
            youtube_download_window.update_idletasks()
            with ytdl.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])
            progress_label.config(text="Download complete!", foreground="green")
            messagebox.showinfo("Success", f"Video successfully downloaded to:\n{folder}")
        except Exception as e:
            progress_label.config(text="An error occurred!", foreground="red")
            messagebox.showerror("Error", f"An error occurred: {str(e)}")

    threading.Thread(target=download_task, daemon=True).start()


#--------------------------------------------------------------------------------------------------------------------------------------------------------
#Function to show Facebook download interface
def show_facebook_download():

    # Define the function to download a video
    def download_video_from_facebook(url):
        if not url:
            messagebox.showerror("Error", "Please enter a valid URL!")
            return

        folder = filedialog.askdirectory()  
        if not folder:
            messagebox.showerror("Error", "No folder selected!")
            return

        options = {
            'format': 'best',
            'outtmpl': f'{folder}/%(title)s.%(ext)s',
            'noplaylist': True, 
            'age_limit': 18,  
            'quiet': False,  
            'referer': 'https://www.facebook.com',  #
        }

        try:
            # Show "Downloading..." status
            status_label.config(text="Downloading... Please wait.", fg="blue")
            facebook_download_window.update_idletasks()  
            with ytdl.YoutubeDL(options) as ydl:
                ydl.download([url])  # Start download
            status_label.config(text="Download completed successfully!", fg="green")
        except Exception as e:
            status_label.config(text=f"Failed to download video! {str(e)}", fg="red")

    global facebook_download_window, download_video_window
    if download_video_window:
        download_video_window.destroy()

    facebook_download_window = tk.Toplevel(root)
    facebook_download_window.title("Download Video from YouTube")
    facebook_download_window.geometry("800x500")
    facebook_download_window.configure(bg="#333333")
    facebook_download_window.attributes('-fullscreen', True)  

    header_frame = tk.Frame(facebook_download_window, bg="#333333", height=100)
    header_frame.pack(fill=X)

    header_label = tk.Label(header_frame, text="Facebook Downloader Tool", font=("Arial", 38, "bold"),bg="#333333",fg="white",)
    header_label.pack(pady=30)

    main_frame = tk.Frame(facebook_download_window, bg="#555555", bd=2, relief="ridge", highlightbackground="#444444", highlightthickness=2, pady=20)
    main_frame.place(relx=0.5, rely=0.5, anchor="center", width=1000, height=600)

    title_label = tk.Label(main_frame, text="Facebook Video Downloader", font=("Helvetica", 30, "bold"), fg="white", bg="#555555")
    title_label.pack(pady=30)

    url_label = tk.Label(main_frame, text="Please enter a valid Facebook URL below:", width=40, font=("Helvetica", 16), fg="white", bg="#555555")
    url_label.pack(pady=10)

    url_entry = tk.Entry(main_frame, font=("Helvetica", 14), width=40)
    url_entry.pack(pady=15)

    ttk_style = tk.ttk.Style()
    ttk_style.configure("success.TButton", font=("Helvetica", 14, "bold"), padding=(0, 10))  
    
    tk.Button(main_frame, text="Download Video", bg="#0078D7", width=15, height=2, fg="white", font=("Helvetica", 14),command=lambda: download_video_from_facebook(url_entry.get())).pack(pady=50)

    global status_label
    status_label = tk.Label(main_frame, text="", font=("Helvetica", 14), fg="white", bg="#555555")
    status_label.pack(pady=10)

    style = ttkb.Style()
    style.configure("success.TButton", font=("Helvetica", 14, "bold"), padding=(0, 10))  

    ttk.Button(facebook_download_window , text="Back", bootstyle=DANGER, command=lambda: [facebook_download_window.destroy(), open_video_window()], width=10).place(relx=0.0, rely=1.0, anchor="sw", x=690, y=-290)  

    ttk.Button(facebook_download_window , text="Exit", bootstyle=DANGER, command=root.quit, width=10).place(relx=1.0, rely=1.0, anchor="se", x=-690, y=-290)  


#------------------------------------------------------------------------------------------------------------------------------------------------------
#Function to show WebSite download interface
def show_website_download():

    # Function to download video from URL
    def download_video_from_website(url):
        url = url_entry.get()  
        if not url:
            messagebox.showerror("Error", "Please enter a valid URL!")
            return

        folder = filedialog.askdirectory()  
        if not folder:
            messagebox.showerror("Error", "No folder selected!")
            return

        options = {
            'format': 'best',  
            'outtmpl': f'{folder}/%(title)s.%(ext)s',  
            'noplaylist': True,  
            'quiet': False,  
        }

        try:
            status_label.config(text="Downloading... Please wait.", fg="blue")
            website_window.update_idletasks()  
            with ytdl.YoutubeDL(options) as ydl:
                ydl.download([url])  
            status_label.config(text="Download completed successfully!", fg="green")
        except Exception as e:
            status_label.config(text=f"Failed to download video! {str(e)}", fg="red")


    global website_window, download_video_window
    if download_video_window:
        download_video_window.destroy()

    website_window = tk.Toplevel(root)
    website_window.title("Download Video from Website")
    website_window.geometry("800x500")
    website_window.configure(bg="#333333")
    website_window.attributes('-fullscreen', True)  

    header_frame = tk.Frame(website_window, bg="#333333", height=100)
    header_frame.pack(fill=X)

    header_label = tk.Label(header_frame, text="Website Downloader Tool", font=("Arial", 38, "bold"),bg="#333333",fg="white",)
    header_label.pack(pady=30)

    main_frame = tk.Frame(website_window, bg="#555555", bd=2, relief="ridge", highlightbackground="#444444", highlightthickness=2, pady=20)
    main_frame.place(relx=0.5, rely=0.5, anchor="center", width=1000, height=600)

    title_label = tk.Label(main_frame, text="Website Video Downloader", font=("Helvetica", 30, "bold"), fg="white", bg="#555555")
    title_label.pack(pady=30)

    url_label = tk.Label(main_frame, text="Please enter a valid Website URL below:", width=40, font=("Helvetica", 16), fg="white", bg="#555555")
    url_label.pack(pady=10)

    url_entry = tk.Entry(main_frame, font=("Helvetica", 14), width=40)
    url_entry.pack(pady=15)

    ttk_style = tk.ttk.Style()
    ttk_style.configure("success.TButton", font=("Helvetica", 14, "bold"), padding=(0, 10))  
    tk.Button(main_frame, text="Download Video", bg="#0078D7", width=15, height=2, fg="white", font=("Helvetica", 14),command=lambda: download_video_from_website(url_entry.get())).pack(pady=50)

    global status_label
    status_label = tk.Label(main_frame, text="", font=("Helvetica", 14), fg="white", bg="#555555")
    status_label.pack(pady=10)

    style = ttkb.Style()
    style.configure("success.TButton", font=("Helvetica", 14, "bold"), padding=(0, 10))  

    ttk.Button(website_window , text="Back", bootstyle=DANGER, command=lambda: [website_window.destroy(), open_video_window()], width=10).place(relx=0.0, rely=1.0, anchor="sw", x=690, y=-290)  

    ttk.Button(website_window , text="Exit", bootstyle=DANGER, command=root.quit, width=10).place(relx=1.0, rely=1.0, anchor="se", x=-690, y=-290)  


#----------------------------------------------------------------------------------------------------------------------------------------------------

# Function to show Audio download interface
def download_audio_window():
    global audio_download_window
    root.withdraw()  
    audio_download_window = ttk.Toplevel(root)
    audio_download_window.title("Download Audio")
    audio_download_window.geometry("600x400")
    audio_download_window.configure(bg="#333333")
    audio_download_window.attributes('-fullscreen', True)  

    header_frame = tk.Frame(audio_download_window, bg="#333333", height=100)
    header_frame.pack(fill=X)

    header_label = tk.Label(header_frame, text="Audio Downloader Tool", font=("Arial", 38, "bold"),bg="#333333",fg="white",)
    header_label.pack(pady=30)

    main_frame = tk.Frame(audio_download_window, bg="#555555", bd=2, relief="ridge", highlightbackground="#444444", highlightthickness=2, pady=20)
    main_frame.place(relx=0.5, rely=0.5, anchor="center", width=1000, height=600)

    title_label = tk.Label(main_frame, text="Audio Downloader", font=("Helvetica", 30, "bold"), fg="white", bg="#555555")
    title_label.pack(pady=30)

    url_label = tk.Label(main_frame, text="Please enter a valid YouTube URL below:", width=40, font=("Helvetica", 16), fg="white", bg="#555555")
    url_label.pack(pady=10)

    url_entry = tk.Entry(main_frame, font=("Helvetica", 14), width=40)
    url_entry.pack(pady=15)

    style = ttkb.Style()
    style.configure("success.TButton", font=("Helvetica", 14, "bold"), padding=(0, 10)) 

    tk.Button(main_frame, text="Download Audio", bg="#0078D7", width=15, height=2, fg="white", font=("Helvetica", 14),command=lambda: start_audio_download(url_entry.get())).pack(pady=50)

    global progress_label_audio
    progress_label_audio = ttk.Label(main_frame, text="", font=("Helvetica", 14), foreground="white")
    progress_label_audio.pack(pady=0)

    ttk.Button(audio_download_window, text="Back", bootstyle=DANGER, command=lambda: [audio_download_window.destroy(), root.deiconify()], width=10).place(relx=0.0, rely=1.0, anchor="sw", x=690, y=-290)

    ttk.Button(audio_download_window, text="Exit", bootstyle=DANGER, command=root.quit, width=10).place(relx=1.0, rely=1.0, anchor="se", x=-690, y=-290)


# Function to handle the download process for audio
def start_audio_download(url):
    def select_folder():
        folder = filedialog.askdirectory(title="Select Folder to Save Audio")
        if not folder:
            messagebox.showwarning("Warning", "No folder selected!")
        return folder

    def download_progress(d):
        if d['status'] == 'downloading':
            percent = d['_percent_str']
            eta = d.get('eta', 'N/A')  
            progress_label_audio.config(text=f"Downloading: {percent} | ETA: {eta}s", foreground="blue")
            audio_download_window.update_idletasks()

    if not url:
        messagebox.showerror("Error", "Please enter a valid audio URL")
        return

    folder = select_folder()
    if not folder:
        return

    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': os.path.join(folder, '%(title)s.%(ext)s'),
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',  
            'preferredquality': '192',  
        }],
        'progress_hooks': [download_progress],
    }

    # Function to run the download process in a separate thread
    def download_task():
        try:
            progress_label_audio.config(text="Preparing download...", foreground="#e62117")
            audio_download_window.update_idletasks()
            with ytdl.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])
            progress_label_audio.config(text="Download complete!", foreground="green")
            messagebox.showinfo("Success", f"Audio successfully downloaded to:\n{folder}")
        except Exception as e:
            progress_label_audio.config(text="An error occurred!", foreground="red")
            messagebox.showerror("Error", f"An error occurred: {str(e)}")

    threading.Thread(target=download_task, daemon=True).start()


#----------------------------------------------------------------------------------------------------------------------------------------------------
#Function to show Playlist download interface
def download_playlist_window():
    global playlist_download_window
    
    root.withdraw()
    playlist_download_window = tk.Toplevel(root)
    playlist_download_window.geometry("600x400")
    playlist_download_window.title("Download Playlist")
    playlist_download_window.configure(bg="#333333")
    playlist_download_window.attributes('-fullscreen', True)  

    header_frame = tk.Frame(playlist_download_window, bg="#333333", height=100)
    header_frame.pack(fill=X)

    header_label = tk.Label(header_frame, text="Playlist Downloader Tool", font=("Arial", 38, "bold"),bg="#333333",fg="white",)
    header_label.pack(pady=30)

    main_frame = tk.Frame(playlist_download_window, bg="#555555", bd=2, relief="ridge", highlightbackground="#444444", highlightthickness=2, pady=20)
    main_frame.place(relx=0.5, rely=0.5, anchor="center", width=1000, height=600)

    title_label = tk.Label(main_frame, text="Playlist Video Downloader", font=("Helvetica", 30, "bold"), fg="white", bg="#555555")
    title_label.pack(pady=30)

    url_label = tk.Label(main_frame, text="Please enter a valid Playlist URL below:", width=40, font=("Helvetica", 16), fg="white", bg="#555555")
    url_label.pack(pady=10)
    
    url_entry = tk.Entry(main_frame, font=("Helvetica", 14), width=40)
    url_entry.pack(pady=15)

    style = ttk.Style()
    style.configure("success.TButton", font=("Helvetica", 14, "bold"), padding=(0, 10))  

    tk.Button(main_frame, text="Download Video", bg="#0078D7", width=15, height=2, fg="white", font=("Helvetica", 14),command=lambda: start_plylist_download(url_entry.get())).pack(pady=50)

    global progress_label
    progress_label = ttk.Label(main_frame, text="", font=("Helvetica", 14), foreground="white")
    progress_label.pack(pady=0)

    ttk.Button(playlist_download_window, text="Back", bootstyle="danger", command=lambda: [playlist_download_window.destroy(), root.deiconify()], width=10).place(relx=0.0, rely=1.0, anchor="sw", x=690, y=-290)
    ttk.Button(playlist_download_window, text="Exit", bootstyle="danger", command=root.quit, width=10).place(relx=1.0, rely=1.0, anchor="se", x=-690, y=-290)
    

# Function to handle the download process
def start_plylist_download(url):
    def select_folder():
        folder = filedialog.askdirectory(title="Select Download Folder", parent=playlist_download_window) 
        if not folder:
            messagebox.showwarning("Warning", "No folder selected!")
        return folder

    def download_playlist(url, folder, progress_label):
        if not url:
            messagebox.showerror("Error", "Please enter a valid playlist URL")
            return

        if not folder:  
            messagebox.showerror("Error", "Please select a valid download folder.")
            return
        
        ydl_opts = {
            'format': 'best',
            'outtmpl': os.path.join(folder, '%(title)s.%(ext)s'),
            'progress_hooks': [lambda d: update_progress(d, progress_label)],
        }

        try:
            progress_label.config(text="Downloading... Please wait.", foreground="blue")
            playlist_download_window.update_idletasks()  
            with YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])  
            progress_label.config(text="Download completed successfully!", foreground="green")
            messagebox.showinfo("Success", "Playlist download complete!")
        except Exception as e:
            progress_label.config(text=f"Failed to download playlist! {str(e)}", foreground="red")
            messagebox.showerror("Error", f"An error occurred: {str(e)}")


    def update_progress(d, progress_label):
        if d['status'] == 'downloading':
            progress_label.config(text=f"Downloading: {d['_percent_str']} completed", foreground="blue")  

    def download_playlist_gui():
        folder = select_folder()
        if folder:  
            progress_label.config(text="Starting download...", foreground="blue")  
            download_playlist(url, folder, progress_label)

    download_playlist_gui()


#-----------------------------------------------------------------------------------------------------------------------------------------------------
# Function to show Extract Images interface
def extract_images_window():
    global extract_image_window
    root.withdraw()
    extract_image_window = ttk.Toplevel(root)
    extract_image_window.geometry("800x500")
    extract_image_window.title("Video Frame Extractor")
    extract_image_window.configure(bg="#333333")
    extract_image_window.resizable(False, False)
    extract_image_window.attributes('-fullscreen', True) 

    def select_video():
        video_path = filedialog.askopenfilename(
            title="Select Video File",
            filetypes=[("Video Files", "*.mp4 *.avi *.mkv *.mov *.flv *.wmv")]
        )
        if video_path:
            video_label.config(text=f"Selected: {os.path.basename(video_path)}")
            return video_path
        else:
            messagebox.showwarning("Warning", "No video file selected!")
            return None

    def extract_image(video_path, time_seconds, output_folder):
        if not os.path.exists(video_path):
            messagebox.showerror("Error", "Invalid video file selected!")
            return
        
        cap = cv2.VideoCapture(video_path)
        fps = cap.get(cv2.CAP_PROP_FPS)
        frame_number = int(fps * time_seconds)

        cap.set(cv2.CAP_PROP_POS_FRAMES, frame_number)
        ret, frame = cap.read()
        if ret:
            image_filename = os.path.join(output_folder, f"frame_at_{time_seconds}s.jpg")
            cv2.imwrite(image_filename, frame)
            cap.release()
            messagebox.showinfo("Success", f"Image saved at {image_filename}")
        else:
            cap.release()
            messagebox.showerror("Error", "Could not extract the frame. Please check the time specified.")

    def extract_image_gui():
        video_path = select_video()
        if not video_path:
            return

        output_folder = filedialog.askdirectory(title="Select Output Folder")
        if not output_folder:
            messagebox.showwarning("Warning", "No output folder selected!")
            return

        try:
            time_seconds = float(time_entry.get())
            if time_seconds < 0:
                raise ValueError
            extract_image(video_path, time_seconds, output_folder)
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid time in seconds!")


    header_frame = tk.Frame(extract_image_window, bg="#333333", height=100)
    header_frame.pack(fill="x")
    header_label = tk.Label(header_frame,text="Extract Image Tool",font=("Arial", 38, "bold"),bg="#333333",fg="white")
    header_label.pack(pady=30)

    content_frame = tk.Frame(extract_image_window, bg="#FFFFFF", padx=250, pady=20)
    content_frame.pack(pady=110)

    title_label = tk.Label(content_frame,text="Video Frame Extractor",font=("Helvetica", 30, "bold"),fg="#444444",bg="#FFFFFF")
    title_label.pack(pady=40)

    instruction_label = tk.Label(content_frame,text="Please select a video to extract an image frame:",font=("Helvetica", 14),fg="#666666",bg="#FFFFFF")
    instruction_label.pack(pady=20)

    video_button = ttk.Button(content_frame, text="Select Video", command=select_video)
    video_button.pack(pady=20)

    video_label = tk.Label(content_frame,text="No video selected",font=("Helvetica", 12),fg="#28a745",bg="#FFFFFF")
    video_label.pack(pady=20)

    time_frame = tk.Frame(content_frame, bg="#FFFFFF")
    time_frame.pack(pady=10)

    time_label = tk.Label(time_frame,text="Enter Time (seconds):",font=("Helvetica", 14),fg="#444444",bg="#FFFFFF")
    time_label.pack(side="left", padx=10)

    time_entry = ttk.Entry(time_frame, font=("Helvetica", 12), width=15)
    time_entry.pack(side="left")

    extract_button = ttk.Button(content_frame, text="Extract Image",command=extract_image_gui)
    extract_button.pack(pady=40)

    ttk.Button(extract_image_window, text="Back", bootstyle=DANGER, command=lambda: [extract_image_window.destroy(), root.deiconify()], width=10).place(relx=0.0, rely=1.0, anchor="sw", x=800, y=-170) 

    ttk.Button(extract_image_window, text="Exit", bootstyle=DANGER, command=root.quit, width=10).place(relx=1.0, rely=1.0, anchor="se", x=-800, y=-170)  

    style = ttk.Style()
    style.configure("TButton", font=("Helvetica", 14), padding=10)
    style.configure("TLabel", font=("Helvetica", 12))

#----------------------------------------------------------------------------------------------------------------------------------------------------
# Function to show Cut Audio interface
def cut_audio():
    global cut_window
    root.withdraw()  
    cut_window = ttk.Toplevel(root)
    cut_window.title("Download Video")
    cut_window.geometry("600x400")  
    cut_window.configure(bg="#333333")
    cut_window.attributes('-fullscreen', True)  

    ttk.Label(cut_window, text="", background="#333333").pack(pady=130)
    ttk.Label(cut_window, text="Select Video Source", font=("Helvetica", 38, "bold"), foreground="white", background="#333333").pack()
    ttk.Label(cut_window, text="", background="#333333").pack(pady=15)

    style = ttkb.Style()
    style.configure("info.TButton",font=("Helvetica", 16, "bold"), padding=(0, 10))  

    ttk.Button(cut_window, text="Cut Audio", bootstyle=INFO, command=lambda: handle_cut_audio(), width=40, style="info.TButton").pack(pady=15)
    ttk.Button(cut_window, text="Cut Video", bootstyle=INFO, command=lambda: handle_cut_video(), width=40, style="info.TButton").pack(pady=15)
    ttk.Button(cut_window, text="Back", bootstyle=DANGER, command=lambda: [cut_window.destroy(), root.deiconify()], width=20, style="danger.TButton").pack(pady=30)


#-----------------------------------------------------------------------------------------------------------------------------------------------------

#Function to handle the Cut Audio of Audio process
def handle_cut_audio():
    # Function to select folder to save cut audio
    def select_folder():
        folder = filedialog.askdirectory()
        if not folder:
            messagebox.showwarning("Warning", "No folder selected!")
        return folder

    # Function to cut audio
    def cut_audio(input_file, start_time, end_time, folder):
        try:
            if not os.path.exists(input_file):
                messagebox.showerror("Error", "The selected audio file does not exist.")
                return

            start_time_ms = start_time * 1000
            end_time_ms = end_time * 1000

            audio = AudioSegment.from_file(input_file)

            if end_time_ms > len(audio):
                messagebox.showerror("Error", "End time exceeds audio length.")
                return

            cut_audio = audio[start_time_ms:end_time_ms]
            base_filename = "cut_audio"
            extension = ".mp3"
            output_filename = os.path.join(folder, f"{base_filename}{extension}")
            counter = 1

            while os.path.exists(output_filename):
                output_filename = os.path.join(folder, f"{base_filename}_{counter}{extension}")
                counter += 1

            cut_audio.export(output_filename, format="mp3")
            messagebox.showinfo("Success", f"Audio cut successfully! Saved as {output_filename}")
            success_label.config(text="Audio cut successfully!", fg="green")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred while cutting the audio: {str(e)}")

    # Function to handle cutting audio
    def cut_audio_gui():
        global selected_file
        if not selected_file:
            messagebox.showerror("Error", "Please select a valid audio file.")
            return

        try:
            start_time = float(start_time_entry.get())
            end_time = float(end_time_entry.get())
        except ValueError:
            messagebox.showerror("Error", "Please enter valid start and end times.")
            return

        folder = select_folder()
        if folder:
            cut_audio(selected_file, start_time, end_time, folder)

    # Function to handle file selection
    def select_file():
        global selected_file
        selected_file = filedialog.askopenfilename(filetypes=[("Audio Files", "*.mp3 *.wav *.flac")])
        if selected_file:
            file_label.config(text=f"Selected File: {os.path.basename(selected_file)}")

    # Function to exit the application
    def exit_app():
        cut_audio_window.destroy()

    # Styling functions for hover effect
    def button_hover_in(e):
        e.widget.config(bg="#FF784E", fg="white")

    def button_hover_out(e):
        e.widget.config(bg="#4CAF50", fg="white")


    # Create the main window of Cut Audio menu
    global cut_audio_window, cut_window
    if cut_window:
        cut_window.destroy()

    cut_audio_window = ttk.Toplevel(root)
    cut_audio_window.geometry("700x600")
    cut_audio_window.title("Audio Cutter")
    cut_audio_window.configure(bg="#333333")
    cut_audio_window.resizable(False, False)
    cut_audio_window.attributes('-fullscreen', True)

    header_frame = tk.Frame(cut_audio_window, bg="#333333", height=100)
    header_frame.pack(fill=X)

    header_label = tk.Label(header_frame, text="Audio Cutter Tool", font=("Arial", 38, "bold"),bg="#333333",fg="white",)
    header_label.pack(pady=30)

    cut_audio_frame = tk.Frame(cut_audio_window, bg="#FFFFFF", padx=250, pady=30)
    cut_audio_frame.pack(pady=100)

    title_label = tk.Label(cut_audio_frame, text="Cut Your Audio File", font=("Arial", 36, "bold"), bg="#FFFFFF", fg="#4CAF50")
    title_label.grid(row=0, column=0, columnspan=2, pady=30)

    description_label = tk.Label(cut_audio_frame, text="Please select a valid audio file (MP3, WAV, FLAC) to cut.",font=("Arial", 11),bg="#FFFFFF",fg="#555555",)
    description_label.grid(row=1, column=0, columnspan=2, pady=20)

    file_button = tk.Button(cut_audio_frame, text="Choose File", command=select_file, font=("Arial", 12), bg="#4CAF50", fg="white", width=15)
    file_button.grid(row=2, column=0, pady=20, padx=10)
    file_button.bind("<Enter>", button_hover_in)
    file_button.bind("<Leave>", button_hover_out)

    file_label = tk.Label(cut_audio_frame, text="No file selected", font=("Arial", 10), bg="#FFFFFF", fg="#555555")
    file_label.grid(row=2, column=1, pady=20, padx=10)

    start_time_label = tk.Label(cut_audio_frame, text="Start Time (seconds):", font=("Arial", 12), bg="#FFFFFF", fg="#4CAF50")
    start_time_label.grid(row=3, column=0, padx=10, pady=20, sticky="e")
    start_time_entry = tk.Entry(cut_audio_frame, font=("Arial", 12), width=20, bg="#F0F0F0", relief="flat")
    start_time_entry.grid(row=3, column=1, pady=20)

    end_time_label = tk.Label(cut_audio_frame, text="End Time (seconds):", font=("Arial", 12), bg="#FFFFFF", fg="#4CAF50")
    end_time_label.grid(row=4, column=0, padx=10, pady=20, sticky="e")
    end_time_entry = tk.Entry(cut_audio_frame, font=("Arial", 12), width=20, bg="#F0F0F0", relief="flat")
    end_time_entry.grid(row=4, column=1, pady=20)

    cut_audio_button = tk.Button(cut_audio_frame,text="Cut Audio",command=cut_audio_gui,font=("Arial", 16, "bold"),bg="#4CAF50",fg="white",relief="raised",width=15,height=1)
    cut_audio_button.grid(row=5, column=0, columnspan=2, pady=45)
    cut_audio_button.bind("<Enter>", button_hover_in)
    cut_audio_button.bind("<Leave>", button_hover_out)

    success_label = tk.Label(cut_audio_frame, text="", font=("Arial", 14, "bold"), bg="#FFFFFF", fg="green")
    success_label.grid(row=6, column=0, columnspan=2, pady=10)

    ttk.Button(cut_audio_window, text="Back", bootstyle=DANGER, command=lambda: go_back_to_cut_audio(), width=10).place(relx=0.0, rely=1.0, anchor="sw", x=800, y=-110)  
    ttk.Button(cut_audio_window, text="Exit", bootstyle=DANGER, command= exit_app, width=10).place(relx=1.0, rely=1.0, anchor="se", x=-800, y=-110) 


#---------------------------------------------------------------------------------------------------------------------------------------------------

#Function to handle the process of Cut audio of Video 
def handle_cut_video():
    # Function to select folder to save cut video
    def select_folder():
        folder = filedialog.askdirectory()
        if not folder:
            messagebox.showwarning("Warning", "No folder selected!")
        return folder

    # Function to cut video
    def cut_video(input_file, start_time, end_time, folder):
        try:
            if not os.path.exists(input_file):
                messagebox.showerror("Error", "The selected video file does not exist.")
                return

            status_label.config(text="Cutting video... Please wait.", fg="blue")
            cut_video_window.update_idletasks()

            with VideoFileClip(input_file) as video:
                if end_time > video.duration:
                    messagebox.showerror("Error", "End time exceeds video length.")
                    return

                cut_video = video.subclip(start_time, end_time)

                base_filename = "cut_video"
                extension = ".mp4"
                output_filename = os.path.join(folder, f"{base_filename}{extension}")
                counter = 1

                while os.path.exists(output_filename):
                    output_filename = os.path.join(folder, f"{base_filename}_{counter}{extension}")
                    counter += 1

                cut_video.write_videofile(output_filename, codec="libx264", audio_codec="aac")
                messagebox.showinfo("Success", f"Video cut successfully! Saved as {output_filename}")

                success_label.config(text="Video cut successfully!", fg="green")

        except Exception as e:
            messagebox.showerror("Error", f"An error occurred while cutting the video: {str(e)}")

    # Function to handle cutting video
    def cut_video_gui():
        input_file = filedialog.askopenfilename(filetypes=[("Video Files", "*.mp4 *.mov *.avi")])
        if not input_file:
            messagebox.showerror("Error", "Please select a valid video file.")
            return

        start_time_entry.config(state='normal')
        end_time_entry.config(state='normal')

        file_button.config(state='disabled')

        file_label.config(text=os.path.basename(input_file))

        cut_video_gui.input_file = input_file

        messagebox.showinfo("Set Time", "Please set the start and end times for the video.")

    # Function to perform the video cutting operation after time input
    def perform_cut():
        input_file = cut_video_gui.input_file
        if not input_file:
            messagebox.showerror("Error", "Please select a valid video file.")
            return

        try:
            start_time = float(start_time_entry.get())
            end_time = float(end_time_entry.get())
        except ValueError:
            messagebox.showerror("Error", "Please enter valid start and end times.")
            return

        folder = select_folder()
        if folder:
            cut_video(input_file, start_time, end_time, folder)

    # Function to exit the application
    def exit_app():
        global cut_video_window
        if cut_video_window:
            cut_video_window.destroy()
            cut_video_window = None

    # Styling functions for hover effect
    def button_hover_in(e):
        e.widget.config(bg="#FF784E", fg="white")

    def button_hover_out(e):
        e.widget.config(bg="#4CAF50", fg="white")

    # Create the main window
    global cut_video_window, cut_window
    if cut_window:
        cut_window.destroy()

    cut_video_window = ttk.Toplevel(root)
    cut_video_window.geometry("700x600")
    cut_video_window.title("Audio Cutter")
    cut_video_window.configure(bg="#333333")
    cut_video_window.resizable(False, False)
    cut_video_window.attributes('-fullscreen', True)

    header_frame = tk.Frame(cut_video_window, bg="#333333", height=100)
    header_frame.pack(fill=X)

    header_label = tk.Label(header_frame,text="Video Cutter Tool",font=("Arial", 38, "bold"),bg="#333333",fg="white",)
    header_label.pack(pady=30)

    cut_video_frame = tk.Frame(cut_video_window, bg="#FFFFFF", padx=250, pady=30)
    cut_video_frame.pack(pady=100)

    title_label = tk.Label(cut_video_frame, text="Cut Your Video File", font=("Arial", 36, "bold"), bg="#FFFFFF", fg="#4CAF50")
    title_label.grid(row=0, column=0, columnspan=2, pady=30)

    description_label = tk.Label(cut_video_frame,text="Please select a valid Video file (MP3, WAV, FLAC) to cut.",font=("Arial", 11),bg="#FFFFFF",fg="#555555",)
    description_label.grid(row=1, column=0, columnspan=2, pady=20)

    file_button = tk.Button(cut_video_frame, text="Choose File", command=cut_video_gui, font=("Arial", 12), bg="#4CAF50", fg="white", width=15)
    file_button.grid(row=2, column=0, pady=20, padx=10)
    file_button.bind("<Enter>", button_hover_in)
    file_button.bind("<Leave>", button_hover_out)

    file_label = tk.Label(cut_video_frame, text="No file selected", font=("Arial", 10), bg="#FFFFFF", fg="#555555")
    file_label.grid(row=2, column=1, pady=20, padx=10)

    start_time_label = tk.Label(cut_video_frame, text="Start Time (seconds):", font=("Arial", 12), bg="#FFFFFF", fg="#4CAF50")
    start_time_label.grid(row=3, column=0, padx=10, pady=20, sticky="e")
    start_time_entry = tk.Entry(cut_video_frame, font=("Arial", 12), width=20, bg="#F0F0F0", relief="flat")
    start_time_entry.grid(row=3, column=1, pady=20)

    end_time_label = tk.Label(cut_video_frame, text="End Time (seconds):", font=("Arial", 12), bg="#FFFFFF", fg="#4CAF50")
    end_time_label.grid(row=4, column=0, padx=10, pady=20, sticky="e")
    end_time_entry = tk.Entry(cut_video_frame, font=("Arial", 12), width=20, bg="#F0F0F0", relief="flat")
    end_time_entry.grid(row=4, column=1, pady=20)

    cut_video_button = tk.Button(cut_video_frame,text="Cut Video",command= perform_cut,font=("Arial", 16, "bold"),bg="#4CAF50",fg="white",relief="raised",width=15,height=1)
    cut_video_button.grid(row=5, column=0, columnspan=2, pady=45)
    cut_video_button.bind("<Enter>", button_hover_in)
    cut_video_button.bind("<Leave>", button_hover_out)

    status_label = tk.Label(cut_video_frame, text="", font=("Arial", 15))
    status_label.grid(row=6, column=0, columnspan=2, pady=10)  

    success_label = tk.Label(cut_video_frame, text="", font=("Arial", 16, "bold"), bg="#FFFFFF", fg="green")
    success_label.grid(row=6, column=0, columnspan=2, pady=10)

    ttk.Button(cut_video_window, text="Back", bootstyle=DANGER, command=lambda: go_back_to_cut_video(), width=10).place(relx=0.0, rely=1.0, anchor="sw", x=800, y=-110)  
    ttk.Button(cut_video_window, text="Exit", bootstyle=DANGER, command=exit_app, width=10).place(relx=1.0, rely=1.0, anchor="se", x=-800, y=-110)  


#---------------------------------------------------------------------------------------------------------------------------------------------------
# Exit the application
def exit_app():
    if messagebox.askyesno("Exit", "Are you sure you want to exit?"):
        root.destroy()

# Function to open the video download window again
def open_video_window():
    global video_window_ref
    video_window_ref = ttk.Toplevel(root)
    video_window_ref.title("Download Video")
    video_window_ref.geometry("600x400")  
    video_window_ref.configure(bg="#333333")
    video_window_ref.attributes('-fullscreen', True)  

    ttk.Label(video_window_ref, text="", background="#333333").pack(pady=130)
    ttk.Label(video_window_ref, text="Select Video Source", font=("Helvetica", 18, "bold"), foreground="white", background="#333333").pack()
    ttk.Label(video_window_ref, text="", background="#333333").pack(pady=15)
    
    style = ttkb.Style()
    style.configure("info.TButton",
                    font=("Helvetica", 16, "bold"),  
                    padding=(0, 10))  

    ttk.Button(video_window_ref, text="YouTube", bootstyle=INFO, command= lambda: show_youtube_download(), width=40, style="info.TButton").pack(pady=15)
    ttk.Button(video_window_ref, text="Facebook", bootstyle=INFO, command=lambda: show_facebook_download(), width=40, style="info.TButton").pack(pady=15)
    ttk.Button(video_window_ref, text="Website", bootstyle=INFO, command=lambda: show_website_download(), width=40, style="info.TButton").pack(pady=15)
    ttk.Button(video_window_ref, text="Back", bootstyle=DANGER, command=lambda: [video_window_ref.destroy(), root.deiconify()], width=20, style="danger.TButton").pack(pady=30)

#-------------------------------------------------------------------------------------------------------------------------------------------------
def go_back_to_cut_audio():
    global cut_audio_window, cut_window

    if cut_audio_window:
       cut_audio_window.destroy()
    cut_audio()

def go_back_to_cut_video():
    global cut_video_window, cut_window
    if cut_video_window:
        cut_video_window.destroy()
    cut_audio()

#---------------------------------------------------------------------------------------------------------------------------------------------------

# Main application window
root = ttk.Window(themename="darkly")  
root.title("Professional Menu Interface")
root.geometry("800x600")  
root.attributes('-fullscreen', True)  

style = ttk.Style()

style.configure("primary.TButton",font=("Helvetica", 14, "bold"),padding=10,relief="flat",  foreground="white")
style.configure("danger.TButton",font=("Helvetica", 14, "bold"),padding=10,relief="flat",background="#DC3545",  foreground="white")

title_frame = ttk.Frame(root, padding=30)
title_frame.pack(fill=X, pady=30)
ttk.Label(title_frame, text="Welcome to the Professional Menu", font=("Helvetica", 38, "bold"), foreground="#ffffff").pack(anchor=CENTER)

menu_frame = ttk.Frame(root, padding=30)
menu_frame.pack(pady=0)

ttk.Button(menu_frame, text="Download Video", bootstyle=PRIMARY, command=download_video, width=50, style="primary.TButton").pack(pady=30, fill=X)
ttk.Button(menu_frame, text="Download Audio", bootstyle=PRIMARY, command=download_audio_window, width=50, style="primary.TButton").pack(pady=30, fill=X)
ttk.Button(menu_frame, text="Download Playlist", bootstyle=PRIMARY, command=download_playlist_window, width=50, style="primary.TButton").pack(pady=30, fill=X)
ttk.Button(menu_frame, text="Extract Image", bootstyle=PRIMARY, command=extract_images_window, width=50, style="primary.TButton").pack(pady=30, fill=X)
ttk.Button(menu_frame, text="Cutter Tool", bootstyle=PRIMARY, command=cut_audio, width=50, style="primary.TButton").pack(pady=30, fill=X)

ttk.Button(root, text="Exit", bootstyle=DANGER, command=exit_app, width=30, style="danger.TButton").pack(pady=30)

root.mainloop()
