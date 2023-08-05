import React, { useState, useEffect, useRef } from 'react';

import WaveSurfer from 'wavesurfer.js';
import TimeLine from 'wavesurfer.js/dist/plugin/wavesurfer.timeline.js';
import Spectrogram from 'wavesurfer.js/dist/plugin/wavesurfer.spectrogram.js';

import colormap from 'colormap';

type AudioProps = { src?: string };

/**
 * @returns The React component
 */
const AudioComponent = (props: AudioProps): JSX.Element => {
  const zoomRange = { min: 1, max: 30000, initial: 1 };
  const fftSamplesArray = [...Array(18)].map((_, i) => Math.pow(2, i));

  const [isPlaying, setPlaying] = useState(false);
  const [zoom, setZoom] = useState(zoomRange.initial);
  //const [fftSamples, setFftSamples] = useState(fftSamplesArray[8]);
  const fftSamples = fftSamplesArray[8];
  // const [keypress, setKeyPress] = useState(false);
  const wavesurferRef = useRef<WaveSurfer>();

  const waveColor = '#4BF2A7';
  const bgColor = 'black';

  const colors = colormap({
    colormap: 'plasma',
    nshades: 256,
    format: 'float'
  });

  // construct wavesurfer
  useEffect(() => {
    if (!wavesurferRef.current) {
      wavesurferRef.current = WaveSurfer.create({
        container: '#waveform',
        waveColor: waveColor,
        backgroundColor: bgColor,
        plugins: [
          TimeLine.create({
            container: '#timeline'
          }),
          Spectrogram.create({
            wavesurfer: wavesurferRef.current,
            container: '#spectrogram',
            labels: true,
            colorMap: colors,
            fftSamples: fftSamples
          })
        ]
      });
    }
  }, [wavesurferRef, colors]);

  // load a wave file
  useEffect(() => {
    const wavesurfer = wavesurferRef.current;
    if (wavesurfer && props.src) {
      wavesurfer.load(props.src);
    }
  }, [wavesurferRef, props.src]);

  // play/pause based on the state
  useEffect(() => {
    const wavesurfer = wavesurferRef.current;
    if (wavesurfer) {
      if (isPlaying) {
        wavesurfer.play();
      } else {
        wavesurfer.pause();
      }
    }
  }, [wavesurferRef, isPlaying]);

  // control zoom
  useEffect(() => {
    const wavesurfer = wavesurferRef.current;
    if (wavesurfer) {
      wavesurfer.zoom(/*pxPerSec=*/ zoom);
    }
  }, [wavesurferRef, zoom]);

  /*
  // space key handling
  const downHandler = e => {
    if (e.key === ' ') {
      setKeyPress(true);
    }
  };
  const upHandler = e => {
    if (e.key === ' ') {
      setKeyPress(false);
    }
  };

  useEffect(() => {
    // register
    window.addEventListener('keydown', downHandler);
    window.addEventListener('keyup', upHandler);

    // cleanup
    return () => {
      window.removeEventListener('keydown', downHandler);
      window.removeEventListener('keyup', upHandler);
    };
  }, []);

  // toggle isPlaying for every keyPress
  useEffect(() => {
    const wavesurfer = wavesurferRef.current;
    if (wavesurfer) {
      if (keypress) {
        setPlaying(!isPlaying);
      }
    }
  }, [wavesurferRef, keypress]);
  */

  return (
    <div style={{ width: '100%' }}>
      <div id="timeline" />
      <div id="waveform" />
      <div id="spectrogram" />
      <button
        onClick={() => {
          isPlaying ? setPlaying(false) : setPlaying(true);
        }}
      >
        {' '}
        Play/Pause{' '}
      </button>
      <div> {isPlaying ? 'Playing' : 'Pause'} </div>
      <div id="zoom">
        <input
          type="range"
          value={zoom}
          onChange={e => setZoom(Number(e.target.value))}
          min={zoomRange.min}
          max={zoomRange.max}
          style={{ width: '100%' }}
        />
        zoom: {zoom} [pixel/sec]
      </div>
      {/*
              <div id="fftSamples">
                    FFT size:
                    <select value={fftSamples} onChange={(e) => setFftSamples(Number(e.target.value))} >
                      {fftSamplesArray.map((value, index) => <option value={value} >{value}</option>)}
                    </select>
              </div>
              */}
    </div>
  );
};

export default AudioComponent;
