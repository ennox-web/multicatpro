import type { Preview } from "@storybook/react";
import React from "react";

import '../src/app/globals.css';
import {roboto} from '../src/app/lib/fonts';

const previewTest: Preview = {
  parameters: {
    controls: {
      matchers: {
        color: /(background|color)$/i,
        date: /Date$/i,
      },
    },
  },
  decorators: [
    (Story) => (
      <div className={`${roboto.className}`}>
        <Story />
      </div>
    ),
  ],
};

export default previewTest;
